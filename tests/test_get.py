from apyshka.api import MyApi, get
from apyshka.request import Request


class TestApi(MyApi):
    root = "http://example.com/api/"

    @get("/thing/{number}/")
    def thing_with_number(self, number=4):
        return Request()


API = TestApi()
req = API.thing_with_number(number=5, other=3)
