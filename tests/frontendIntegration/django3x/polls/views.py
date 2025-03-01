# Copyright (c) 2021, VRAI Labs and/or its affiliates. All rights reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License") as published by the Apache Software Foundation.
#
# You may not use this file except in compliance with the License. You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import json
import os
import sys
from functools import wraps
from typing import Union
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from supertokens_python import init, Supertokens, SupertokensConfig, InputAppInfo
from supertokens_python.recipe import session
from supertokens_python.recipe.session import SessionRecipe, InputErrorHandlers, Session
from supertokens_python.recipe.session.framework.django.asyncio import verify_session
from supertokens_python.recipe.session.asyncio import revoke_all_sessions_for_user, create_new_session, get_session

module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, '../templates/index.html')
print(file_path)
index_file = open(file_path, "r")
file_contents = index_file.read()
index_file.close()

os.environ.setdefault('SUPERTOKENS_ENV', 'testing')

last_set_enable_anti_csrf = True
last_set_enable_jwt = False


def custom_decorator_for_test():
    def session_verify_custom_test(f):
        @wraps(f)
        async def wrapped_function(request, *args, **kwargs):
            Test.increment_attempted_refresh()
            try:
                value = await f(request, *args, **kwargs)
                if value is not None and value.status_code != 200:
                    return value
                if request.headers.get("rid") is None:
                    return HttpResponse(content='refresh failed')
                Test.increment_refresh()
                return HttpResponse(content='refresh success')
            except Exception as e:
                raise e

        return wrapped_function

    return session_verify_custom_test


def custom_decorator_for_update_jwt():
    def session_verify_custom_test(f):
        @wraps(f)
        async def wrapped_function(request, *args, **kwargs):
            if request.method == 'GET':
                Test.increment_get_session()
                value = await f(request, *args, **kwargs)
                if value is not None and value.status_code != 200:
                    return value
                session = request.supertokens
                resp = JsonResponse(session.get_access_token_payload())
                resp['Cache-Control'] = 'no-cache, private'
                return resp
            else:
                if request.method == 'POST':
                    value = await f(request, *args, **kwargs)
                    if value is not None and value.status_code != 200:
                        return value
                    session = request.supertokens
                    await session.update_access_token_payload(json.loads(request.body))
                    Test.increment_get_session()
                    resp = JsonResponse(session.get_access_token_payload())
                    resp['Cache-Control'] = 'no-cache, private'
                    return resp
            return send_options_api_response()

        return wrapped_function

    return session_verify_custom_test


def custom_decorator_for_get_info():
    def session_verify_custom_test(f):
        @wraps(f)
        async def wrapped_function(request, *args, **kwargs):
            if request.method == 'GET':
                value = await f(request, *args, **kwargs)
                if value is not None and value.status_code != 200:
                    return value
                Test.increment_get_session()
                session = request.supertokens
                resp = HttpResponse(session.get_user_id())
                resp['Cache-Control'] = 'no-cache, private'
                return resp
            else:
                return send_options_api_response()

        return wrapped_function

    return session_verify_custom_test


def custom_decorator_for_logout():
    def session_verify_custom_test(f):
        @wraps(f)
        async def wrapped_function(request, *args, **kwargs):
            if request.method == 'POST':
                value = await f(request, *args, **kwargs)
                if value is not None and value.status_code != 200:
                    return value
                session = request.supertokens
                await session.revoke_session()
                return HttpResponse('success')
            return send_options_api_response()

        return wrapped_function

    return session_verify_custom_test


def try_refresh_token(_):
    return HttpResponse(json.dumps(
        {'error': 'try refresh token'}), content_type="application/json", status=401)


def unauthorised(_):
    return HttpResponse(json.dumps(
        {'error': 'unauthorised'}), content_type="application/json", status=401)


class Test:
    no_of_times_refresh_called_during_test = 0
    no_of_times_get_session_called_during_test = 0
    no_of_times_refresh_attempted_during_test = 0

    @staticmethod
    def reset():
        Test.no_of_times_refresh_called_during_test = 0
        Test.no_of_times_get_session_called_during_test = 0
        Test.no_of_times_refresh_attempted_during_test = 0

    @staticmethod
    def increment_refresh():
        Test.no_of_times_refresh_called_during_test = Test.no_of_times_refresh_called_during_test + 1

    @staticmethod
    def increment_attempted_refresh():
        Test.no_of_times_refresh_attempted_during_test = Test.no_of_times_refresh_attempted_during_test + 1

    @staticmethod
    def increment_get_session():
        Test.no_of_times_get_session_called_during_test = Test.no_of_times_get_session_called_during_test + 1

    @staticmethod
    def get_session_called_count():
        return Test.no_of_times_get_session_called_during_test

    @staticmethod
    def get_refresh_called_count():
        return Test.no_of_times_refresh_called_during_test

    @staticmethod
    def get_refresh_attempted_count():
        return Test.no_of_times_refresh_attempted_during_test


async def unauthorised_f(error, req, res):
    res.set_status_code(401)
    res.set_json_content({})


def apis_override_session(param):
    param.disable_refresh_post = True
    return param


def functions_override_session(param):
    original_create_new_session = param.create_new_session

    async def create_new_session_custom(request: any, user_id: str, access_token_payload: Union[dict, None] = None,
                                        session_data: Union[dict, None] = None) -> Session:
        if access_token_payload is None:
            access_token_payload = {}
        access_token_payload = {
            **access_token_payload,
            'customClaim': 'customValue'
        }
        return await original_create_new_session(request, user_id, access_token_payload, session_data)
    param.create_new_session = create_new_session_custom

    return param


def get_app_port():
    argvv = sys.argv
    for i in range(0, len(argvv)):
        if argvv[i] == '--port':
            return argvv[i + 1]

    return '8080'


def config(enable_anti_csrf: bool, enable_jwt: bool, jwt_property_name: Union[str, None]):
    anti_csrf: Literal['VIA_TOKEN', 'NONE'] = "NONE"
    if enable_anti_csrf:
        anti_csrf = "VIA_TOKEN"
    if enable_jwt:
        init(
            supertokens_config=SupertokensConfig('http://localhost:9000'),
            app_info=InputAppInfo(
                app_name="SuperTokens Python SDK",
                api_domain="0.0.0.0:" + get_app_port(),
                website_domain="http://localhost.org:8080"
            ),
            framework='django',
            mode='asgi',
            recipe_list=[session.init(
                error_handlers=InputErrorHandlers(
                    on_unauthorised=unauthorised_f
                ),
                anti_csrf=anti_csrf,
                override=session.InputOverrideConfig(
                    apis=apis_override_session,
                    functions=functions_override_session
                ),
                jwt=session.JWTConfig(enable_jwt, jwt_property_name)
            )],
            telemetry=False
        )
    else:
        init(
            supertokens_config=SupertokensConfig('http://localhost:9000'),
            app_info=InputAppInfo(
                app_name="SuperTokens Python SDK",
                api_domain="0.0.0.0:" + get_app_port(),
                website_domain="http://localhost.org:8080"
            ),
            framework='django',
            mode='asgi',
            recipe_list=[session.init(
                error_handlers=InputErrorHandlers(
                    on_unauthorised=unauthorised_f
                ),
                anti_csrf=anti_csrf,
                override=session.InputOverrideConfig(
                    apis=apis_override_session
                )
            )],
            telemetry=False
        )


config(True, False, None)


async def send_file(request):
    return render(request, file_path)


async def send_options_api_response():
    return HttpResponse('')


async def login(request):
    if request.method == 'POST':
        user_id = json.loads(request.body)['userId']

        session_ = await create_new_session(request, user_id)
        return HttpResponse(session_.get_user_id())
    else:
        return send_options_api_response()


async def before_each(request):
    if request.method == 'POST':
        Test.reset()
        return HttpResponse('')
    else:
        return send_options_api_response()


async def test_config(request):
    if request.method == 'POST':
        return HttpResponse('')
    else:
        return send_options_api_response()


async def multiple_interceptors(request):
    if request.method == 'POST':
        result_bool = 'success' if 'interceptorheader2' in request.headers \
                                   and 'interceptorheader1' in request.headers else 'failure'
        return HttpResponse(result_bool)
    else:
        return send_options_api_response()


@custom_decorator_for_get_info()
@verify_session()
async def get_info(request):
    return HttpResponse('')


@custom_decorator_for_update_jwt()
@verify_session()
async def update_jwt(request):
    return HttpResponse('')


async def testing(request):
    if request.method in ['GET', 'PUT', 'POST', 'DELETE']:
        if 'testing' in request.headers:
            resp = HttpResponse('success')
            resp['testing'] = request.headers['testing']
            return resp
        return HttpResponse("success")

    # options
    return send_options_api_response()


@custom_decorator_for_logout()
@verify_session()
async def logout(request):
    return HttpResponse('')


@verify_session()
async def revoke_all(request):
    if request.method:
        session = await get_session(request)
        await revoke_all_sessions_for_user(session.get_user_id())
        return HttpResponse('success')
    else:
        return send_options_api_response()


async def refresh_attempted_time(request):
    if request.method == 'GET':
        return HttpResponse(Test.get_refresh_attempted_count())
    else:
        return send_options_api_response()


@custom_decorator_for_test()
@verify_session()
async def refresh(request):
    return HttpResponse(content='refresh success')


def set_anti_csrf(request):
    global last_set_enable_anti_csrf
    data = json.loads(request.body)
    if "enableAntiCsrf" not in data:
        enable_csrf = True
    else:
        enable_csrf = data["enableAntiCsrf"]

    last_set_enable_anti_csrf = enable_csrf
    if enable_csrf is not None:
        Supertokens.reset()
        SessionRecipe.reset()
        config(enable_csrf, False, None)
    return HttpResponse('success')


def set_enable_jwt(request):
    global last_set_enable_jwt
    global last_set_enable_anti_csrf
    data = json.loads(request.body)
    if "enableJWT" not in data:
        enable_jwt = False
    else:
        enable_jwt = data["enableJWT"]

    last_set_enable_jwt = enable_jwt
    if enable_jwt is not None:
        Supertokens.reset()
        SessionRecipe.reset()
        config(last_set_enable_anti_csrf, enable_jwt, None)
    return HttpResponse('success')


def feature_flags(request):
    global last_set_enable_jwt
    return JsonResponse({
        'sessionJwt': last_set_enable_jwt
    })


async def reinitialize(request):
    global last_set_enable_jwt
    global last_set_enable_anti_csrf
    data = json.loads(request.body)
    if "jwtPropertyName" not in data:
        jwt_property_name = True
    else:
        jwt_property_name = data["jwtPropertyName"]

    Supertokens.reset()
    SessionRecipe.reset()
    config(last_set_enable_anti_csrf, last_set_enable_jwt, jwt_property_name)
    return HttpResponse('')


async def refresh_called_time(request):
    if request.method == 'GET':
        return HttpResponse(Test.get_refresh_called_count())
    else:
        return send_options_api_response()


async def get_session_called_time(request):
    if request.method == 'GET':
        return HttpResponse(str(Test.get_session_called_count()))
    else:
        return send_options_api_response()


async def ping(request):
    if request.method == 'GET':
        return HttpResponse('success')
    else:
        return send_options_api_response()


async def test_header(request):
    if request.method == 'GET':
        success_info = request.headers.get('st-custom-header')
        return JsonResponse({'success': success_info})
    else:
        return send_options_api_response()


async def check_device_info(request):
    if request.method == 'GET':
        sdk_name = request.headers.get('supertokens-sdk-name')
        sdk_version = request.headers.get('supertokens-sdk-version')
        return HttpResponse('true' if sdk_name == 'website' and isinstance(
            sdk_version, str) else 'false')
    else:
        return send_options_api_response()


async def check_rid(request):
    rid = request.headers.get('rid')
    return HttpResponse('fail' if rid is None else 'success')


async def check_allow_credentials(request):
    if request.method == 'GET':
        return JsonResponse(json.dumps('allow-credentials' in request.headers))
    else:
        return send_options_api_response()


async def test_error(request):
    if request.method == 'OPTIONS':
        return send_options_api_response()
    return HttpResponse('test error message', status=500)

# @app.exception_handler(405)
# def f_405(_, e):
#     return PlainTextResponse('', status_code=404)


# cors middleware added like this due to issue with add_middleware
# ref: https://github.com/tiangolo/fastapi/issues/1663
