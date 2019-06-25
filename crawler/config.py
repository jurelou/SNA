FACEBOOK_CREDENTIALS = ("email address", "password")
NEO4J_CREDENTIALS = ("uri", "user", "password")


def test_config():
        # FACEBOOK_CREDENTIALS
    assert isinstance(FACEBOOK_CREDENTIALS, tuple)
    assert len(FACEBOOK_CREDENTIALS) == 2
    assert isinstance(FACEBOOK_CREDENTIALS[0], str)
    assert isinstance(FACEBOOK_CREDENTIALS[1], str)
    # NEO4J_CREDENTIALS
    assert isinstance(NEO4J_CREDENTIALS, tuple)
    assert len(NEO4J_CREDENTIALS) == 3
    assert isinstance(NEO4J_CREDENTIALS[0], str)
    assert isinstance(NEO4J_CREDENTIALS[1], str)
    assert isinstance(NEO4J_CREDENTIALS[2], str)
    print("Config is OK")


if __name__ == "__main__":
    test_config()
