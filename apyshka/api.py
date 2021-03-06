import re
from urllib.parse import urlencode, urlparse, urlunparse

import requests

from apyshka.url_pattern_processor import get_url_pattern_tokens


class Apyshka:
    root = None


    def __init__(self, domain):
        if self.root is None:
            raise ValueError("Need to specify api root")
        self.domain = domain
        self.session = self.prepare_session()


    def prepare_session(self):
        return requests.Session()


def get(pattern):
    def make_http_call(self, inner_pattern, params, query):
        url = make_url(self, inner_pattern, params, query)
        return self.session.get(url)
    return wrapper_maker(pattern, make_http_call)


def post(pattern, encoding="json"):
    def make_http_call(self, inner_pattern, params, query):
        url = make_url(self, inner_pattern, params, {})
        if encoding == "json":
            data_dict = {"json": query}
        else:
            data_dict = {"data": query}
        return self.session.post(url, **data_dict)
    return wrapper_maker(pattern, make_http_call)


def wrapper_maker(pattern, http_call_fn):
    def wrapper(fn):
        url_pattern_params = get_url_pattern_tokens(fn, pattern)

        def inner_wrapper(self, *args, **kwargs):
            kwargs_processor = KwargsProcessor(url_pattern_params)
            params, query = kwargs_processor.process(args, kwargs)
            response = fn(self, *args, **kwargs)
            if not response:
                response = http_call_fn(self, pattern, params, query)
                if response.ok:
                    return response.json()
                raise Exception(response.status_code)
            return response

        return inner_wrapper
    return wrapper


def make_url(self, pattern, params, query):
    parts = list(urlparse(self.domain))
    parts[2] = make_url_path(self.root, pattern, params)
    parts[4] = urlencode(query, doseq=True)
    return urlunparse(parts)


def make_url_path(api_root, pattern, params):
    populated_pattern = pattern.format(**params)
    url_path = "/".join([api_root, populated_pattern])
    return re.sub("/{2,}", "/", url_path)


class KwargsProcessor:
    def __init__(self, url_pattern_params):
        self.url_pattern_params = url_pattern_params
        self.query = {}
        self.params = {}


    def process(self, args, kwargs):
        self.look_for_query_in_kwargs(kwargs)
        self.look_for_params(args, kwargs)
        raise_if_not_dicts(self.query, self.params)
        return self.params, self.query


    def look_for_query_in_kwargs(self, kwargs):
        self.query = kwargs.pop("q", {})


    def look_for_params(self, args, kwargs):
        self.look_for_params_in_kwargs(kwargs)
        self.look_for_one_param_in_args(args, self.url_pattern_params, kwargs)
        self.use_kwargs_as_params(kwargs)
        self.check_params_against_url()


    def look_for_params_in_kwargs(self, kwargs):
        params = kwargs.pop("params", {})
        if not isinstance(params, dict):
            raise ValueError("Params must be a dictionary")
        self.params = params


    def look_for_one_param_in_args(self, args, path_params, kwargs):
        raise_if_both(self.params, args)
        if args:
            if len(args) == 1 and len(path_params) == 1 and not kwargs:
                self.params = {path_params[0]: args[0]}
            else:
                raise ValueError(
                    "args only allowed if there is one path param,"
                    " and only one arg can be present"
                )


    def use_kwargs_as_params(self, kwargs):
        if not self.params and not self.query:
            self.params = kwargs


    def check_params_against_url(self):
        if list(self.params.keys()) != self.url_pattern_params:
            raise ValueError("Params are not the same as parameters in the path")


def raise_if_not_dicts(query, params):
    if not isinstance(query, dict) or not isinstance(params, dict):
        raise ValueError("params and q parameters must be dictionaries")


def raise_if_both(params, args):
    if params and args:
        raise ValueError(
            "A non-named param is allowed only if `params` argument is not present"
        )
