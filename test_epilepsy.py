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
        expected = images[i][1]
        got = safegif.process_gif(images[i][0])
        success = expected is got
        print(f"{expected} expected, got {got}: {'✓' if success else '✖'}")


if __name__ == '__main__':
    main()


def test_epilepsy_triggering():
    images = [
        "test_images/epilepsy.gif",
        "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_a770d1805b514b97956c9695508e0d44/default/dark/3.0",
        "https://webaim.org/articles/seizure/media/flicker.gif",
        "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_502bf8fd256b44348d9a5b9c546bee67/default/dark/3.0"
    ]
    for i in range(len(images)):
        assert safegif.process_gif(images[i])


def test_epilepsy_safe():
    images = [
        "test_images/normal.gif",
        "https://webaim.org/articles/seizure/media/illusion.gif"
    ]
    for i in range(len(images)):
        assert not safegif.process_gif(images[i])
