import inspect
from contextlib import suppress
from string import Formatter


def get_url_pattern_tokens(api_function, url_pattern):
    api_call_params = get_declared_params(api_function)
    url_pattern_params = _get_path_params(url_pattern)
    check_fn_params_with_url_pattern(api_call_params, url_pattern_params)
    return url_pattern_params


def check_fn_params_with_url_pattern(api_call_params, url_pattern_params):
    if len(set(url_pattern_params)) != len(api_call_params):
        # Check that they contain the same values
        raise ValueError("Pattern must not contain duplicate params")


def get_declared_params(fn):
    all_params = inspect.getfullargspec(fn)[0]
    with suppress(ValueError):
        all_params.remove("self")
    return all_params


def _get_path_params(path_pattern):
    if not path_pattern:
        return []
    path_field_names = []
    for x in Formatter().parse(path_pattern):
        if x[1]:
            path_field_names.append(x[1])
    return path_field_names
