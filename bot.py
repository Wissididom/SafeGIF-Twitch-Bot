import os.path
import json
import requests
import websocket
import time
import rel
from threading import Thread

import api as safegif

alreadySubscribedToEvent = False
tokens = {
  'access_token': None,
  'refresh_token': None,
  'device_code': None,
  'user_code': None,
  'verification_uri': None,
  'user_id': None
}

class Bot:
    def __init__(self, client_id: str, client_secret: str, scopes: str, initial_channels: list[str], whisper_on_deletion: bool,
                 whisper_text: str = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.initial_channels = initial_channels
        self.whisper_on_deletion = whisper_on_deletion
        self.whisper_text = whisper_text

    def validation_loop(self):
        while True:
            time.sleep(60 * 60) # Sleep for one hour
            self.validate_token()

    def run(self) -> bool:
        global tokens
        if os.path.isfile('.tokens.json'):
            with open('.tokens.json') as token_file:
                tokens = json.load(token_file)
            validated = self.validate_token()
            if validated:
                Thread(daemon = True, target = self.validation_loop).start()
                self.connect_eventsub()
                return True
            else:
                return False
        else:
            dcf_response = requests.post(f"https://id.twitch.tv/oauth2/device?client_id={self.client_id}&scopes={self.scopes}")
            dcf = None
            if dcf_response.ok:
                dcf = dcf_response.json()
            if dcf is None:
                print(f"DCF Response Status Code is not below 400 (Status Code: {dcf_response.status_code})")
                return False
            tokens['device_code'] = dcf['device_code']
            tokens['user_code'] = dcf['user_code']
            tokens['verification_uri'] = dcf['verification_uri']
            print(f"Open {tokens['verification_uri']} and enter {tokens['user_code']} there!")
            token_response = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={self.client_id}&scope={self.scopes}&device_code={dcf['device_code']}&grant_type=urn:ietf:params:oauth:grant-type:device_code")
            while token_response.status_code == 400:
                time.sleep(5)
                token_response = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={self.client_id}&scope={self.scopes}&device_code={dcf['device_code']}&grant_type=urn:ietf:params:oauth:grant-type:device_code")
            if token_response.ok:
                token_json = token_response.json()
                tokens['access_token'] = token_json['access_token']
                tokens['refresh_token'] = token_json['refresh_token']
                tokens['user_id'] = self.get_twitch_user()['id']
            if tokens is None:
                print(f"Token Response Status Code is not below 400 (Status Code: {token_response.status_code})")
                return False
            with open('.tokens.json', 'w') as fp:
                json.dump(tokens, fp)
            Thread(daemon = True, target = self.validation_loop).start()
            self.connect_eventsub()
            return True

    def connect_eventsub(self):
        # websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://eventsub.wss.twitch.tv/ws",
                              on_open=self.on_open,
                              on_message=self.on_message,
                              on_error=self.on_error,
                              on_close=self.on_close)
        ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
        rel.signal(2, rel.abort)  # Keyboard Interrupt
        rel.dispatch()

    def on_open(self, ws):
        print("EventSub connection established!")

    def on_close(self, ws, close_status_code, close_msg):
        print("EventSub connection closed!")

    def on_error(self, ws, error):
        print(error)

    def on_message(self, ws, message) -> None:
        global alreadySubscribedToEvent, tokens
        data = json.loads(message)
        if data['metadata']['message_type'] == 'session_welcome':
            print(f"session_welcome: {json.dumps(data)}")
            if alreadySubscribedToEvent:
                return
            id = data['payload']['session']['id']
            for initial_channel in self.initial_channels:
                subscription = self.create_eventsub_subscription('channel.chat.message', '1', {'broadcaster_user_id': self.get_twitch_user(initial_channel.lower())['id'], 'user_id': tokens['user_id']}, id)
                print(f'{initial_channel}-Subscription: {subscription.status_code}: {subscription.text}')
            alreadySubscribedToEvent = True
        elif data['metadata']['message_type'] == 'session_keepalive':
            print(f"session_keepalive: {json.dumps(data)}")
        elif data['metadata']['message_type'] == 'session_reconnect':
            print(f"session_reconnect: {json.dumps(data)}")
            ws2 = websocket.WebSocketApp(data['payload']['session']['reconnect_url'],
                              on_open=self.on_open,
                              on_message=self.on_message,
                              on_error=self.on_error,
                              on_close=self.on_close)
            ws2.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
            ws.close()
            ws = ws2
            rel.signal(2, rel.abort)  # Keyboard Interrupt
            rel.dispatch()
        elif data['payload']['subscription']['type'] == 'channel.chat.message':
            print(f"channel.chat.message: {json.dumps(data)}")
            # https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types/#channelchatmessage
            # https://dev.twitch.tv/docs/eventsub/eventsub-reference/#channel-chat-message-event
            chat_message_event = data['payload']['event']
            for fragment in chat_message_event['message']['fragments']:
                if fragment['type'] == 'cheermote':
                    # https://dev.twitch.tv/docs/api/reference/#get-cheermotes
                    cheermotes = self.get_cheermotes(chat_message_event['broadcaster_user_id']).json()['data']
                    for cheermote in cheermotes:
                        if cheermote['prefix'] != fragment['cheermote']['prefix']:
                            continue
                        for tier in cheermote['tiers']:
                            self.handle_safegif(tier['dark']['animated']['4'], chat_message_event['broadcaster_user_id'], tokens['user_id'], chat_message_event['chatter_user_id'], chat_message_event['message_id'])
                            self.handle_safegif(tier['light']['animated']['4'], chat_message_event['broadcaster_user_id'], tokens['user_id'], chat_message_event['chatter_user_id'], chat_message_event['message_id'])
                if fragment['type'] == 'emote':
                    for fmt in fragment['emote']['format']:
                        if fmt == 'static':
                            continue
                        self.handle_safegif(f'https://static-cdn.jtvnw.net/emoticons/v2/{fragment['emote']['id']}/{fmt}/light/3.0', chat_message_event['broadcaster_user_id'], tokens['user_id'], chat_message_event['chatter_user_id'], chat_message_event['message_id'])
                        self.handle_safegif(f'https://static-cdn.jtvnw.net/emoticons/v2/{fragment['emote']['id']}/{fmt}/dark/3.0', chat_message_event['broadcaster_user_id'], tokens['user_id'], chat_message_event['chatter_user_id'], chat_message_event['message_id'])
        else:
            print(f"EventSub Data: {json.dumps(data)}")

    def handle_safegif(self, url: str, broadcaster_id: str, moderator_id: str, user_id: str, message_id: str):
        if safegif.process_gif(url):
            print(f'{url} - True')
            response = self.delete_chat_message(broadcaster_id, moderator_id, message_id)
            if response.status_code == 204:
                print('Successfully deleted message')
                if self.whisper_text is not None and self.whisper_on_deletion:
                    response = self.send_whisper(moderator_id, user_id, self.whisper_text)
                    if response.status_code == 204:
                        print(f'Successfully sent or silently dropped whisper message to ID {user_id}')
                    else:
                        print(f'Error sending whisper: {response.status_code}: {response.text}')
            else:
                print('Failed to delete the message!')
        else:
            print(f'{url} - False')

    def get_cheermotes(self, broadcaster_id: str):
        return self.get(f'https://api.twitch.tv/helix/bits/cheermotes?broadcaster_id={broadcaster_id}')

    def get(self, url: str, firstTry: bool = True):
        global tokens
        response = requests.get(url, headers={'Client-ID': self.client_id, 'Authorization': f'Bearer {tokens['access_token']}'})
        if response.status_code == 401 and firstTry:
            self.refresh_token()
            return self.get(url, False)
        return response

    def post(self, url: str, json = None, firstTry: bool = True):
        global tokens
        response = None
        if json is None:
            response = requests.post(url, headers={'Client-ID': self.client_id, 'Authorization': f'Bearer {tokens['access_token']}'})
        else:
            response = requests.post(url, headers={'Client-ID': self.client_id, 'Authorization': f'Bearer {tokens['access_token']}'}, json=json)
        if response.status_code == 401 and firstTry:
            self.refresh_token()
            return self.post(url, json, False)
        return response

    def delete(self, url: str, firstTry: bool = True):
        global tokens
        response = requests.delete(url, headers={'Client-ID': self.client_id, 'Authorization': f'Bearer {tokens['access_token']}'})
        if response.status_code == 401 and firstTry:
            self.refresh_token()
            return self.delete(url, False)
        return response

    def refresh_token(self):
        global tokens
        refresh_result = self.post(
            f'https://id.twitch.tv/oauth2/token?client_id={self.client_id}&client_secret={self.client_secret}&grant_type=refresh_token&refresh_token={tokens.refresh_token}')
        if token.status_code == 401: # Refresh failed
            # TODO: Start new DCF
            print("Refreshing tokens failed")
            return
        refresh_json = refresh_result.json()
        if refresh_result.status_code >= 200 and refresh_result.status_code < 300:
            # Successfully refreshed
            tokens['access_token'] = refresh_json['access_token']
            tokens.refresh_token = refresh_json['refresh_token']
            with open('.tokens.json', 'w') as fp:
                json.dump(tokens, fp)
            print('Successfully refreshed tokens!')
            return True
        else:
            # Refresh failed
            print(f'Failed refreshing tokens: {json.dump(refresh_json)}')
            return False

    def validate_token(self):
        global tokens
        res = self.get(
            'https://id.twitch.tv/oauth2/validate')
        if res.status_code is None:
            print(f'Unhandled network error! res.status_code is None {res}')
            return False
        if res.status_code == 401:
            return refresh_token()
        elif res.status_code >= 200 and res.status_code < 300:
            print('Successfully validated tokens!')
            return True
        else:
            print(f'Unhandled validation error: {json.dump(res.json())}')
            return False
        json = token.json()
        tokens['access_token'] = json['access_token']
        tokens.refresh_token = json['refresh_token']
        with open('.tokens.json', 'w') as fp:
            json.dump(tokens, fp)

    def get_twitch_user(self, login: str = None):
        if login is None:
            return self.get('https://api.twitch.tv/helix/users').json()['data'][0]
        else:
            return self.get(f'https://api.twitch.tv/helix/users?login={login}').json()['data'][0]

    def create_eventsub_subscription(self, subscription_type: str, version: str, condition, session_id: str):
        return self.post(
            'https://api.twitch.tv/helix/eventsub/subscriptions', {
                'type': subscription_type,
                'version': version,
                'condition': condition,
                'transport': {
                    'method': 'websocket',
                    'session_id': session_id
                }
            })

    def delete_chat_message(self, broadcaster_id: str, moderator_id: str, message_id: str):
        return self.delete(
            f'https://api.twitch.tv/helix/moderation/chat?broadcaster_id={broadcaster_id}&moderator_id={moderator_id}&message_id={message_id}')

    def send_whisper(self, from_user_id: str, to_user_id: str, message: str):
        return self.post(f'https://api.twitch.tv/helix/whispers?from_user_id={from_user_id}&to_user_id={to_user_id}', json={'message': message})
