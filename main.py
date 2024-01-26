import os
import urllib.parse

from dotenv import load_dotenv

from bot import Bot

load_dotenv()

TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID', 'byvo5xr9mepepi9km69nfab44jbglk')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET', None)
INITIAL_CHANNELS = os.getenv('INITIAL_CHANNELS')
WHISPER_ON_DELETION = True
WHISPER_TEXT = os.getenv('WHISPER_TEXT',
                         'Your message included an emote that could be triggering epilepsy so it was deleted')
SCOPES = urllib.parse.quote('user:read:chat user:write:chat moderator:manage:chat_messages user:manage:whispers')


def main():
    global TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, INITIAL_CHANNELS, SCOPES, WHISPERS_ON_DELETION, WHISPER_TEXT
    if INITIAL_CHANNELS is None:
        INITIAL_CHANNELS = input(
            "Please enter the name of the channels you want the bot to monitor (separated by comma): ").strip()
    bot = Bot(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, SCOPES, INITIAL_CHANNELS.split(','), WHISPER_ON_DELETION, WHISPER_TEXT)
    bot.run()


if __name__ == '__main__':
    main()
