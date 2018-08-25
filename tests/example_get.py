from functools import partial

from apyshka.api import Apyshka, get, post
from apyshka.util import retry


class ExampleApi(Apyshka):
    root = "/posts/"

    @get("{number}")
    def get_a_post(self, number=1) -> dict:
        pass

    @post("/thing/{numero}", "form")
    def post_thing_with_number(self, numero=5) -> {}:
        pass


API = ExampleApi("https://jsonplaceholder.typicode.com/")
# req = API.thing_with_number(params={"number": 5}, q={"one": "two"})


# API.thing_with_number(3)
# API.retry(5).thing_with_number(3)
# print(">>>")

dct = retry(
    partial(API.get_a_post, 1),
    # lambda: API.get_a_post(1),
    times=3, sleep=4
)
# API.post_thing_with_number(7, q={"something": "In the way she moves"})


