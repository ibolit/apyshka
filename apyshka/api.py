import inspect
from contextlib import suppress
from string import Formatter

from apyshka.request import Request


class MyApi:
    root = None


    def __init__(self):
        if self.root is None:
            print("Need to specify api root")


def get(pattern):
    def wrapper(fn):
        print(pattern)
        params_processor = ParamsProcessor(fn, pattern)

        def inner_wrapper(self, *args, **kwargs):
            kwargs_processor = KwargsProcessor(params_processor.url_pattern_params)
            params, query = kwargs_processor.process(args, kwargs)
            request = fn(self, *args, **kwargs)
            if not request:
                request = Request()
                request.url = pattern.format(**params)
                request.query(**query)
            return request

        return inner_wrapper
    return wrapper


class ParamsProcessor:
    def __init__(self, api_function, url_pattern):
        self.api_call_params = self.get_declared_params(api_function)
        self.url_pattern_params = self.get_path_params(url_pattern)


    def check_fn_params_with_url_pattern(self):
        if len(set(self.url_pattern_params)) != len(self.api_call_params):
            # Check that they contain the same values
            raise ValueError("Pattern must not contain duplicate params")


    def get_declared_params(self, fn):
        all_params = inspect.getfullargspec(fn)[0]
        with suppress(ValueError):
            all_params.remove("self")
        return all_params


    def get_path_params(self, path_pattern):
        if not path_pattern:
            return []
        path_field_names = []
        for x in Formatter().parse(path_pattern):
            if x[1]:
                path_field_names.append(x[1])
        return path_field_names


class KwargsProcessor:
    def __init__(self, url_pattern_params):
        self.url_pattern_params = url_pattern_params
        self.query = {}
        self.params = {}


    def process(self, args, kwargs):
        self.look_for_query_in_kwargs(kwargs)
        self.look_for_params(args, kwargs)
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
        raise_if_not_dicts(self.query, self.params)


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
