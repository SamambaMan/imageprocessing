from pytest import fixture


@fixture
def postdata():
    return """{
        "operations": [
            ["resize", "200x300"],
            ["split", true],
            ["blur", "gaussian"],
    ["blur", "gaussian"],
    ["split", true]
        ],
        "output":"jpg"
    }"""
