import sys
import traceback
from twitchio.ext import commands
from twitchio import Message
import api as safegif
import requests
import os


def delete_chat_message(client_id: str, access_token: str, broadcaster_id: str, moderator_id: str, message_id: str):
    return requests.delete(
        f'https://api.twitch.tv/helix/moderation/chat?broadcaster_id={broadcaster_id}&moderator_id={moderator_id}&message_id={message_id}', headers={
            'Client-ID': client_id,
            'Authorization': f'Bearer {access_token}'
        })


class Bot(commands.Bot):
    def __init__(self, access_token: str):
        super().__init__(token=access_token, prefix='safegifbot', initial_channels=[os.getenv('INITIAL_CHANNEL')])
        self.access_token = access_token

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as {self.nick}')
        print(f'User id is {self.user_id}')

    async def event_message(self, message: Message) -> None:
        emotes_str = message.tags.get('emotes')
        if emotes_str is None:
            emotes_str = ''
        if emotes_str.strip() == '':
            return
        emotes = [emote.split(":")[0] for emote in emotes_str.replace('/', ',').split(',')]
        # print(emotes_str)
        # print(emotes)
        for emote in emotes:
            try:
                if safegif.process_gif(f'https://static-cdn.jtvnw.net/emoticons/v2/{emote}/default/dark/3.0'):
                    print(f'https://static-cdn.jtvnw.net/emoticons/v2/{emote}/default/dark/3.0 - True')
                    response = requests.get('https://id.twitch.tv/oauth2/validate', headers={
                        'Authorization': f'OAuth {self.access_token}'
                    })
                    if response.status_code == 200:
                        response = delete_chat_message(
                            client_id=os.getenv('TWITCH_CLIENT_ID'),
                            access_token=self.access_token,
                            broadcaster_id=(await message.channel.user()).id,
                            moderator_id=self.user_id,
                            message_id=message.tags.get('id')
                        )
                        if response.status_code == 204:
                            print('Successfully deleted message')
                    else:
                        print('Failed to delete the message. Exiting...')
                        sys.exit()
                    break
                else:
                    print(f'https://static-cdn.jtvnw.net/emoticons/v2/{emote}/default/dark/3.0 - False')
            except ValueError:
                print(f'https://static-cdn.jtvnw.net/emoticons/v2/{emote}/default/dark/3.0 - ValueError')
                traceback.print_exc()
