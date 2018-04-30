from apyshka.api import Apyshka, get
from apyshka.util import retry


class TestApi(Apyshka):
    root = "/api/"

    @get("/thing/{number}/")
    def thing_with_number(self, number=4):
        return {}


API = TestApi("https://example.com/")
# req = API.thing_with_number(params={"number": 5}, q={"one": "two"})


# API.thing_with_number(3)
# API.retry(5).thing_with_number(3)
print(">>>")

dct = retry(
    lambda: API.thing_with_number(3),
    times=3, sleep=4
)
