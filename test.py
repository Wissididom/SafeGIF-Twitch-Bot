from dotenv import load_dotenv

import api as safegif

load_dotenv()


def main():
    print(safegif.process_gif('epilepsy.gif'))
    print(safegif.process_gif('normal.gif'))
    print(safegif.process_gif(
        'https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_a770d1805b514b97956c9695508e0d44/default/dark/3.0'))
    print(safegif.process_gif('https://webaim.org/articles/seizure/media/flicker.gif'))
    print(safegif.process_gif('https://webaim.org/articles/seizure/media/illusion.gif'))


if __name__ == '__main__':
    main()
