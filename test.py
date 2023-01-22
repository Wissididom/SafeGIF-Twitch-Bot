import api as safegif


def main():
    images = [
        "test_images/epilepsy.gif",
        "test_images/normal.gif",
        "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_a770d1805b514b97956c9695508e0d44/default/dark/3.0",
        "https://webaim.org/articles/seizure/media/flicker.gif",
        "https://webaim.org/articles/seizure/media/illusion.gif",
        "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_502bf8fd256b44348d9a5b9c546bee67/default/dark/3.0"
    ]
    for i in range(len(images)):
        print(safegif.process_gif(images[i]))


if __name__ == '__main__':
    main()
