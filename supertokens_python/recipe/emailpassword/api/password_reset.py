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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from supertokens_python.recipe.emailpassword.interfaces import APIOptions, APIInterface
from .utils import validate_form_fields_or_throw_error
from supertokens_python.exceptions import raise_bad_input_exception


async def handle_password_reset_api(api_implementation: APIInterface, api_options: APIOptions):
    if api_implementation.disable_generate_password_reset_token_post:
        return None
    body = await api_options.request.json()
    form_fields_raw = body['formFields'] if 'formFields' in body else []
    form_fields = await validate_form_fields_or_throw_error(api_options.config.reset_password_using_token_feature.form_fields_for_password_reset_form,
                                                            form_fields_raw)

    if 'token' not in body:
        raise_bad_input_exception('Please provide the password reset token')
    if not isinstance(body['token'], str):
        raise_bad_input_exception('The password reset token must be a string')

    token = body['token']
    response = await api_implementation.password_reset_post(form_fields, token, api_options)
    api_options.response.set_json_content(response.to_json())

    return api_options.response
