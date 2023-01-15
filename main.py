from bot import Bot
from dotenv import load_dotenv
import os
import webbrowser

load_dotenv()

TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID', 'byvo5xr9mepepi9km69nfab44jbglk')
TWITCH_REDIRECT_URI = os.getenv('TWITCH_REDIRECT_URI', 'https://pasteme.local/')
INITIAL_CHANNELS = os.getenv('INITIAL_CHANNELS')
WHISPERS_ON_DELETION = True
WHISPER_TEXT = os.getenv('WHISPER_TEXT', 'Your message included an emote that could be triggering epilepsy so it was deleted')
SCOPES = 'chat%3Aread+chat%3Aedit+moderator%3Amanage%3Achat_messages+user%3Amanage%3Awhispers'


def main():
    global TWITCH_CLIENT_ID, TWITCH_REDIRECT_URI, INITIAL_CHANNELS, SCOPES, WHISPERS_ON_DELETION, WHISPER_TEXT
    if INITIAL_CHANNELS is None:
        INITIAL_CHANNELS = input("Please enter the name of the channels you want the bot to monitor (separated by comma): ").strip()
    webbrowser.open(f"https://id.twitch.tv/oauth2/authorize?client_id={TWITCH_CLIENT_ID}&redirect_uri={TWITCH_REDIRECT_URI}&response_type=token&scope={SCOPES}&force_verify=true")
    print("After you've authorized you get redirected to a non-existent page. Please copy+paste the url below!")
    url = input('Paste the url twitch redirects you to here: ').strip()
    access_token = url.split('#')[1].split('=')[1].split('&')[0]
    bot = Bot(TWITCH_CLIENT_ID, access_token, INITIAL_CHANNELS.split(','), WHISPERS_ON_DELETION, WHISPER_TEXT)
    bot.run()


if __name__ == '__main__':
    main()
