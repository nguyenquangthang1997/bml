from aiohttp.web import json_response


def success(response_data, **kwargs):
    return json_response({**kwargs, "status": "success", "data": response_data})


def fail(message, status=200, **kwargs):
    response_data = {"message": message}
    return json_response(
        {**kwargs, "status": "fail", "data": response_data}, status=status
    )
