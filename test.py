import api as safegif


def main():
    images = [
        ("test_images/epilepsy.gif", True),
        ("test_images/normal.gif", False),
        ("https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_a770d1805b514b97956c9695508e0d44/default/dark/3.0", True),
        ("https://webaim.org/articles/seizure/media/flicker.gif", True),
        ("https://webaim.org/articles/seizure/media/illusion.gif", False),
        ("https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_502bf8fd256b44348d9a5b9c546bee67/default/dark/3.0", True)
    ]
    for i in range(len(images)):
        print(f"{images[i][1]} expected, got {safegif.process_gif(images[i][0])}")


if __name__ == '__main__':
    main()
