FACEBOOK_CREDENTIALS = ("email", "password")


def test_config():
    assert isinstance(FACEBOOK_CREDENTIALS, tuple)
    assert len(FACEBOOK_CREDENTIALS) == 2
    assert isinstance(FACEBOOK_CREDENTIALS[0], str)
    assert isinstance(FACEBOOK_CREDENTIALS[1], str)
    print("Config is OK")


if __name__ == "__main__":
    test_config()
