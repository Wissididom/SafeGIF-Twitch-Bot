from bot import Bot
# import api as SafeGIF
from dotenv import load_dotenv
import os
import webbrowser

load_dotenv()


def main():
    # print(SafeGIF.process_gif('epilepsy.gif'))
    # print(SafeGIF.process_gif('normal.gif'))
    # print(SafeGIF.process_gif('https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_a770d1805b514b97956c9695508e0d44/default/dark/3.0'))
    webbrowser.open(f"https://id.twitch.tv/oauth2/authorize?client_id={os.getenv('TWITCH_CLIENT_ID')}&redirect_uri={os.getenv('TWITCH_REDIRECT_URI')}&response_type=token&scope=chat%3Aread+chat%3Aedit+moderator%3Amanage%3Achat_messages")
    print("After you've authorized you get redirected to a non-existent page. Please copy+paste the url below!")
    url = input('Paste the url twitch redirects you to here: ')
    access_token = url.split('#')[1].split('=')[1].split('&')[0]
    bot = Bot(access_token)
    bot.run()


if __name__ == '__main__':
    main()
