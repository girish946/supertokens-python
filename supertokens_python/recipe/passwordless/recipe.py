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
from __future__ import annotations

from os import environ
from typing import List, TYPE_CHECKING, Union, Callable, Awaitable
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from supertokens_python.querier import Querier
from .api import (
    consume_code,
    create_code,
    resend_code,
    email_exists,
    phone_number_exists
)
from .api.implementation import APIImplementation
from .constants import CREATE_CODE_API, RESEND_CODE_API, CONSUME_CODE_API, DOES_EMAIL_EXIST_API, \
    DOES_PHONE_NUMBER_EXIST_API
from .interfaces import APIOptions
from .recipe_implementation import RecipeImplementation
from .utils import validate_and_normalise_user_input, OverrideConfig, ContactConfig
from .exceptions import SuperTokensPasswordlessError
from .interfaces import ConsumeCodeOkResult

if TYPE_CHECKING:
    from supertokens_python.framework.request import BaseRequest
    from supertokens_python.framework.response import BaseResponse
    from supertokens_python.supertokens import AppInfo

from supertokens_python.exceptions import SuperTokensError, raise_general_exception
from supertokens_python.normalised_url_path import NormalisedURLPath
from supertokens_python.recipe_module import RecipeModule, APIHandled


class PasswordlessRecipe(RecipeModule):
    recipe_id = 'passwordless'
    __instance = None

    def __init__(self, recipe_id: str, app_info: AppInfo, contact_config: ContactConfig,
                 flow_type: Literal['USER_INPUT_CODE', 'MAGIC_LINK', 'USER_INPUT_CODE_AND_MAGIC_LINK'],
                 override: Union[OverrideConfig, None] = None,
                 get_link_domain_and_path: Union[Callable[[str], Awaitable[Union[str, None]]]] = None,
                 get_custom_user_input_code: Union[Callable[[], Awaitable[str]], None] = None):
        super().__init__(recipe_id, app_info)
        self.config = validate_and_normalise_user_input(app_info, contact_config, flow_type, override,
                                                        get_link_domain_and_path, get_custom_user_input_code)

        recipe_implementation = RecipeImplementation(Querier.get_instance(recipe_id))
        self.recipe_implementation = recipe_implementation if self.config.override.functions is None else \
            self.config.override.functions(recipe_implementation)
        api_implementation = APIImplementation()
        self.api_implementation = api_implementation if self.config.override.apis is None else \
            self.config.override.apis(api_implementation)

    def get_apis_handled(self) -> List[APIHandled]:
        return [
            APIHandled(method='post', path_without_api_base_path=NormalisedURLPath(CONSUME_CODE_API),
                       request_id=CONSUME_CODE_API,
                       disabled=self.api_implementation.disable_consume_code_post),
            APIHandled(method='post', path_without_api_base_path=NormalisedURLPath(CREATE_CODE_API),
                       request_id=CREATE_CODE_API,
                       disabled=self.api_implementation.disable_create_code_post),
            APIHandled(method='get', path_without_api_base_path=NormalisedURLPath(DOES_EMAIL_EXIST_API),
                       request_id=DOES_EMAIL_EXIST_API,
                       disabled=self.api_implementation.disable_email_exists_get),
            APIHandled(method='get', path_without_api_base_path=NormalisedURLPath(DOES_PHONE_NUMBER_EXIST_API),
                       request_id=DOES_PHONE_NUMBER_EXIST_API,
                       disabled=self.api_implementation.disable_phone_number_exists_get),
            APIHandled(method='post', path_without_api_base_path=NormalisedURLPath(RESEND_CODE_API),
                       request_id=RESEND_CODE_API,
                       disabled=self.api_implementation.disable_resend_code_post)
        ]

    async def handle_api_request(self, request_id: str, request: BaseRequest, path: NormalisedURLPath, method: str,
                                 response: BaseResponse):
        options = APIOptions(request, response, self.get_recipe_id(), self.config, self.recipe_implementation)
        if request_id == CONSUME_CODE_API:
            return await consume_code(self.api_implementation, options)
        elif request_id == CREATE_CODE_API:
            return await create_code(self.api_implementation, options)
        elif request_id == DOES_EMAIL_EXIST_API:
            return await email_exists(self.api_implementation, options)
        elif request_id == DOES_PHONE_NUMBER_EXIST_API:
            return await phone_number_exists(self.api_implementation, options)
        return await resend_code(self.api_implementation, options)

    async def handle_error(self, request: BaseRequest, err: SuperTokensError, response: BaseResponse):
        raise err

    def get_all_cors_headers(self):
        return []

    def is_error_from_this_recipe_based_on_instance(self, err):
        return isinstance(err, SuperTokensError) and isinstance(err, SuperTokensPasswordlessError)

    @staticmethod
    def init(contact_config: ContactConfig,
             flow_type: Literal['USER_INPUT_CODE', 'MAGIC_LINK', 'USER_INPUT_CODE_AND_MAGIC_LINK'],
             override: Union[OverrideConfig, None] = None,
             get_link_domain_and_path: Union[Callable[[str], Awaitable[Union[str, None]]]] = None,
             get_custom_user_input_code: Union[Callable[[], Awaitable[str]], None] = None):
        def func(app_info: AppInfo):
            if PasswordlessRecipe.__instance is None:
                PasswordlessRecipe.__instance = PasswordlessRecipe(
                    PasswordlessRecipe.recipe_id,
                    app_info,
                    contact_config, flow_type, override,
                    get_link_domain_and_path, get_custom_user_input_code)
                return PasswordlessRecipe.__instance
            else:
                raise_general_exception('Passwordless recipe has already been initialised. Please check '
                                        'your code for bugs.')

        return func

    @staticmethod
    def get_instance() -> PasswordlessRecipe:
        if PasswordlessRecipe.__instance is not None:
            return PasswordlessRecipe.__instance
        raise_general_exception(
            'Initialisation not done. Did you forget to call the SuperTokens.init function?')

    @staticmethod
    def reset():
        if ('SUPERTOKENS_ENV' not in environ) or (
                environ['SUPERTOKENS_ENV'] != 'testing'):
            raise_general_exception(
                'calling testing function in non testing env')
        PasswordlessRecipe.__instance = None

    async def create_magic_link(self, email: Union[str, None], phone_number: Union) -> str:
        user_input_code = None
        if self.config.get_custom_user_input_code is not None:
            user_input_code = await self.config.get_custom_user_input_code()

        code_info = await self.recipe_implementation.create_code(
            email=email, phone_number=phone_number, user_input_code=user_input_code)
        magic_link = await self.config.get_link_domain_and_path(email if email is not None else phone_number)
        magic_link += '?rid=' + self.get_recipe_id() + '&preAuthSessionId=' + code_info.pre_auth_session_id + '#' + \
            code_info.link_code
        return magic_link

    async def signinup(self, email: Union[str, None], phone_number: Union) -> ConsumeCodeOkResult:
        code_info = await self.recipe_implementation.create_code(
            email=email, phone_number=phone_number)
        consume_code_result = await self.recipe_implementation.consume_code(
            link_code=code_info.link_code,
            pre_auth_session_id=code_info.pre_auth_session_id,
            device_id=code_info.device_id,
            user_input_code=code_info.user_input_code
        )
        if consume_code_result.is_ok:
            return ConsumeCodeOkResult(consume_code_result.created_new_user, consume_code_result.user)
        else:
            raise Exception('Failed to create user. Please retry')
