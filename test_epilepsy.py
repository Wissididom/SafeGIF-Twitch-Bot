import api as safegif


def main():
    images = [
        ("test_images/epilepsy.gif", True),
        ("test_images/normal.gif", False),
        ("https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_a770d1805b514b97956c9695508e0d44/default/dark/3.0", True),
        ("https://webaim.org/articles/seizure/media/flicker.gif", True),
        ("https://webaim.org/articles/seizure/media/illusion.gif", False),
        ("https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_502bf8fd256b44348d9a5b9c546bee67/default/dark/3.0", True),
        # ("https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_a0f0d42f9001456281d9fbc37a6081b2/default/dark/3.0", False),
        ("https://media.tenor.com/Jt9XZCbBEnkAAAAd/khosalis-snail.gif", True),
        ("https://media.tenor.com/y_v9qSrp4ckAAAAC/moving-art.gif", True),
        ("https://media.tenor.com/IUmIvOuUzMAAAAAd/disco-distracted.gif", True),
        ("https://media.tenor.com/yzwcdxxlnqYAAAAi/hmmm-thinking.gif", False),
        # ("https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_5169f685980a4c11b71f913bbf9d25d6/default/dark/3.0", False),
        ("https://i.pinimg.com/originals/19/81/9e/19819ebc0065a496ef95a8069ad0dc76.gif", False),
        ("https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_d30b413bc2c04591b2eab8c20bdc7627/default/dark/3.0", True),
        ("https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_63cdcc8a9e2f4f71a6223ea6b98df920/default/dark/3.0", True),
        ("https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_95626eb72c644ad1a2d2f99ce3c4f606/default/dark/3.0", True),
        ("https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_c1bc896c0fa74c01b2dad226dcfe41d5/default/dark/3.0", True),
        ("https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_7790e6239f7b4630aba88e63dc19da60/default/dark/3.0", True)
    ]
    for i in range(len(images)):
        expected = images[i][1]
        got = safegif.process_gif(images[i][0])
        success = expected is got
        print(f"{expected} expected, got {got}: {'✓' if success else '✖'} - {images[i][0]}")


if __name__ == '__main__':
    main()


def test_epilepsy_triggering():
    images = [
        "test_images/epilepsy.gif",
        "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_a770d1805b514b97956c9695508e0d44/default/dark/3.0",
        "https://webaim.org/articles/seizure/media/flicker.gif",
        "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_502bf8fd256b44348d9a5b9c546bee67/default/dark/3.0",
        "https://media.tenor.com/Jt9XZCbBEnkAAAAd/khosalis-snail.gif",
        "https://media.tenor.com/y_v9qSrp4ckAAAAC/moving-art.gif",
        "https://media.tenor.com/IUmIvOuUzMAAAAAd/disco-distracted.gif",
        "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_d30b413bc2c04591b2eab8c20bdc7627/default/dark/3.0",
        "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_63cdcc8a9e2f4f71a6223ea6b98df920/default/dark/3.0",
        "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_95626eb72c644ad1a2d2f99ce3c4f606/default/dark/3.0",
        "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_c1bc896c0fa74c01b2dad226dcfe41d5/default/dark/3.0",
        "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_7790e6239f7b4630aba88e63dc19da60/default/dark/3.0"
    ]
    for i in range(len(images)):
        assert safegif.process_gif(images[i])


def test_epilepsy_safe():
    images = [
        "test_images/normal.gif",
        "https://webaim.org/articles/seizure/media/illusion.gif",
        # "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_a0f0d42f9001456281d9fbc37a6081b2/default/dark/3.0",
        "https://media.tenor.com/yzwcdxxlnqYAAAAi/hmmm-thinking.gif",
        # "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_5169f685980a4c11b71f913bbf9d25d6/default/dark/3.0",
        "https://i.pinimg.com/originals/19/81/9e/19819ebc0065a496ef95a8069ad0dc76.gif"
    ]
    for i in range(len(images)):
        assert not safegif.process_gif(images[i])
