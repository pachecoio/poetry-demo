from functools import wraps

from flask import jsonify, make_response, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from api.exceptions import ApiError


def parse_with(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            form_data = request.form
            if form_data:
                data = {}
                for key in form_data.keys():
                    if form_data.getlist(key) and len(form_data.getlist(key)) > 1:
                        data[key] = form_data.getlist(key)
                    else:
                        data[key] = form_data[key]
            else:
                data = request.get_json()
            try:
                entity = schema.load(data)
            except ValidationError as err:
                if args:
                    api_error = args[0]
                    if isinstance(api_error, ApiError):
                        return make_response(
                            jsonify({"error": True, "message": api_error.message}),
                            api_error.status_code,
                        )
                return make_response(
                    jsonify({"error": True, "message": err.messages}), 400
                )
            return f(*args, entity=entity, **kwargs)

        return decorated_function

    return decorator


def get_status_code_success(method):
    if method == "POST":
        return 201
    if method == "DELETE":
        return 202
    return 200


def marshal_with(schema, template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                status_code = get_status_code_success(request.method)
                entity = schema.dump(f(*args, **kwargs))
                res = {"success": True, "error": False, "data": entity}
                if template:
                    template["data"][template["name"]] = entity
                    entity = template["data"]
                if isinstance(entity, dict):
                    status_code = entity.get("status_code", status_code)
                res["status_code"] = status_code
                return make_response(jsonify(res), status_code)
            except IntegrityError as err:
                print("error found")
                return make_response(
                    jsonify(
                        {
                            "error": True,
                            "success": False,
                            "message": err.orig.pgerror,
                        }
                    ),
                    400,
                )

        return decorated_function

    return decorator


def parse_request(arguments):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = dict(**kwargs)
            params = request.args
            for argument in arguments:
                if argument.append:
                    data[argument.name] = [
                        argument.type(param)
                        for param in params.getlist(argument.name) or []
                    ]
                elif params.get(argument.name):
                    data[argument.name] = argument.type(params.get(argument.name))
                elif argument.default:
                    data[argument.name] = argument.default
                elif argument.required:
                    return (
                        jsonify(
                            error=True,
                            messages="Parameter {} is required".format(argument.name),
                        ),
                        400,
                    )
            return f(*args, **data)

        return decorated_function

    return decorator


class Argument(object):
    def __init__(self, name, default=None, type=str, required=False, append=False):
        self.name = name
        self.default = default
        self.type = type
        self.required = required
        self.append = append
