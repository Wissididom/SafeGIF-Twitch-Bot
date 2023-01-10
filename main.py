from bot import Bot
from dotenv import load_dotenv
import os
import webbrowser

load_dotenv()


def main():
    webbrowser.open(f"https://id.twitch.tv/oauth2/authorize?client_id={os.getenv('TWITCH_CLIENT_ID')}&redirect_uri={os.getenv('TWITCH_REDIRECT_URI')}&response_type=token&scope=chat%3Aread+chat%3Aedit+moderator%3Amanage%3Achat_messages+user%3Amanage%3Awhispers")
    print("After you've authorized you get redirected to a non-existent page. Please copy+paste the url below!")
    url = input('Paste the url twitch redirects you to here: ')
    access_token = url.split('#')[1].split('=')[1].split('&')[0]
    bot = Bot(access_token)
    bot.run()


if __name__ == '__main__':
    main()
