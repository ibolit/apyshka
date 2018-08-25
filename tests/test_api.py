from unittest import TestCase

import pytest
from hamcrest import assert_that, calling, equal_to, raises, has_entry, instance_of
from mock import MagicMock

from apyshka.api import Apyshka, KwargsProcessor, get, post


class TestKwargsProcessor_W_1_UrlParam(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.processor = KwargsProcessor(["hello"])


    def test_w_args(self):
        """arg and path params correct"""
        actual = self.processor.process([2], {})
        assert_that(actual, equal_to(({"hello": 2}, {})))


    def test_w_just_dict_params(self):
        actual = self.processor.process([], {"params": {"hello": 2}})
        assert_that(actual, equal_to(({"hello": 2}, {})))


    def test_w_just_dict_params_and_query(self):
        actual = self.processor.process([], {"params": {"hello": 2}, "q": {"page": 3}})
        assert_that(actual, equal_to(({"hello": 2}, {"page": 3})))


    def test_w_just_dict_params_and_query_and_arg(self):
        """Cannot call with arg and params"""
        assert_that(
            calling(self.processor.process).with_args(
                [3], {"params": {"hello": 2}, "q": {"page": 3}}
            ),
            raises(ValueError)
        )

    def test_w_query_not_dict(self):
        """Cannot call with arg and params"""
        assert_that(
            calling(self.processor.process).with_args(
                [3], {"q": 2}
            ),
            raises(ValueError)
        )

    def test_w_wrong_param(self):
        """Cannot call with arg and params"""
        assert_that(
            calling(self.processor.process).with_args(
                [], {"bye": 2}
            ),
            raises(ValueError)
        )


class TestKwargsProcessor_W_ParamsParam(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.processor = KwargsProcessor(["params"])


    def test_w_params_not_dict(self):
        """Cannot call with arg and params"""
        assert_that(
            calling(self.processor.process).with_args(
                [], {"params": 2}
            ),
            raises(ValueError)
        )


class TestWithTwoParams(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.processor = KwargsProcessor(["hello", "bye"])

    def test_w_more_path_params(self):
        """More path params than api call params"""
        assert_that(
            calling(
                self.processor.process
            ).with_args(
                [2], {}
            ),
            raises(ValueError)
        )


    def test_w_more_api_call_params(self):
        """More than 1 api call params"""
        assert_that(
            calling(
                self.processor.process
            ).with_args(
                [2, 8], {}
            ),
            raises(ValueError)
        )


class MyApi(Apyshka):
    root = "/v1/"

    @get("posts/{number}")
    def get_post(self, number) -> {}:
        pass


    @post("posts/", encoding="form")
    def create_post(self):
        pass


    @post("comments/", encoding="json")
    def create_comment(self):
        pass


    def prepare_session(self):
        return MagicMock()


@pytest.fixture
def api():
    return MyApi("http://localhost")


class TestTheApi:
    def test_get_decorator(self, api):
        api.get_post(10)
        assert_that(
            api.session.get.call_args[0][0],
            equal_to("http://localhost/v1/posts/10")
        )


    def test_post_decorator(self, api):
        api.create_post(q={"post_name": "Post", "contents": "some contents of the post"})
        assert_that(
            api.session.post.call_args[0][0],
            equal_to("http://localhost/v1/posts/")
        )
        assert_that(
            api.session.post.call_args[1], {
                'data': {
                    'post_name': 'Post', 'contents':
                        'some contents of the post'
                }
            }
        )


    def test_post_decorator_with_json(self, api):
        api.create_comment(q={"post_name": "Post"})
        assert_that(
            api.session.post.call_args[1],
            has_entry("json", instance_of(dict))
        )
