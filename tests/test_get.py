from apyshka.api import Apyshka, get


class TestApi(Apyshka):
    root = "/api/"

    @get("/thing/{number}/")
    def thing_with_number(self, number=4):
        raise Exception()
        return {}


API = TestApi("https://example.com/")
# req = API.thing_with_number(params={"number": 5}, q={"one": "two"})


API.thing_with_number(3)
print(">>>")
