from flask import request

from exceptions.request_exceptions import MissingParameterException


def get_params(action: str, param_lst: list[str]):
    params = list()
    for param in param_lst:
        if param not in request.args:
            raise MissingParameterException(action=action, param=param)
        params.append(request.args[param])
    return params
