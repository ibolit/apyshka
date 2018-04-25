import re
from urllib.parse import urlencode, urlparse, urlunparse

from apyshka.url_pattern_processor import get_url_pattern_tokens


class Apyshka:
    root = None


    def __init__(self, domain):
        if self.root is None:
            raise ValueError("Need to specify api root")
        self.domain = domain


def get(pattern):
    def wrapper(fn):
        print(pattern)
        url_pattern_params = get_url_pattern_tokens(fn, pattern)

        def inner_wrapper(self, *args, **kwargs):
            kwargs_processor = KwargsProcessor(url_pattern_params)
            params, query = kwargs_processor.process(args, kwargs)
            request = fn(self, *args, **kwargs)
            if not request:
                url = make_url(self, pattern, params, query)
                print(url)
            return request

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
        self.params = kwargs.pop("params", {})


    def look_for_one_param_in_args(self, args, path_params, kwargs):
        raise_if_both(self.params, args)
        if args:
            if len(args) == 1 and len(path_params) == 1 and not kwargs:
                self.params = {path_params[0]: args[0]}
            else:
                raise ValueError("args only allowed if there is one path param, and only one arg can be present")


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
        raise ValueError("A non-named param is allowed only if `params` argument is not present")
