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

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Union

from supertokens_python.types import APIResponse
from typing_extensions import Literal

if TYPE_CHECKING:
    from supertokens_python.framework import BaseRequest, BaseResponse

    from .types import User
    from .utils import EmailVerificationConfig


class CreateEmailVerificationTokenResult(ABC):
    def __init__(
            self, status: Literal['OK', 'EMAIL_ALREADY_VERIFIED_ERROR'], token: Union[str, None]):
        self.status: Literal['OK', 'EMAIL_ALREADY_VERIFIED_ERROR'] = status
        self.is_ok: bool = False
        self.is_email_already_verified: bool = False
        self.token: Union[str, None] = token


class CreateEmailVerificationTokenOkResult(CreateEmailVerificationTokenResult):
    def __init__(self, token: str):
        super().__init__('OK', token)
        self.is_ok = True
        self.is_email_already_verified = False


class CreateEmailVerificationTokenEmailAlreadyVerifiedErrorResult(
        CreateEmailVerificationTokenResult):
    def __init__(self):
        super().__init__('EMAIL_ALREADY_VERIFIED_ERROR', None)
        self.is_ok = False
        self.is_email_already_verified = True


class VerifyEmailUsingTokenOkResult:
    def __init__(self, user: User):
        self.user = user


class VerifyEmailUsingTokenInvalidTokenErrorResult:
    pass


class RevokeEmailVerificationTokensResult(ABC):
    def __init__(self, status: Literal['OK']):
        self.status = status


class RevokeEmailVerificationTokensOkResult(
        RevokeEmailVerificationTokensResult):
    def __init__(self):
        super().__init__('OK')
        self.is_ok = True


class UnverifyEmailResult(ABC):
    def __init__(self, status: Literal['OK']):
        self.status = status
        self.is_ok = False


class UnverifyEmailOkResult(UnverifyEmailResult):
    def __init__(self):
        super().__init__('OK')
        self.is_ok = True


class RecipeInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def create_email_verification_token(self, user_id: str, email: str, user_context: Dict[str, Any]) -> Union[CreateEmailVerificationTokenOkResult, CreateEmailVerificationTokenEmailAlreadyVerifiedErrorResult]:
        pass

    @abstractmethod
    async def verify_email_using_token(self, token: str, user_context: Dict[str, Any]) -> Union[VerifyEmailUsingTokenOkResult, VerifyEmailUsingTokenInvalidTokenErrorResult]:
        pass

    @abstractmethod
    async def is_email_verified(self, user_id: str, email: str, user_context: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def revoke_email_verification_tokens(self, user_id: str, email: str, user_context: Dict[str, Any]) -> RevokeEmailVerificationTokensResult:
        pass

    @abstractmethod
    async def unverify_email(self, user_id: str, email: str, user_context: Dict[str, Any]) -> UnverifyEmailResult:
        pass


class APIOptions:
    def __init__(self, request: BaseRequest, response: BaseResponse, recipe_id: str,
                 config: EmailVerificationConfig, recipe_implementation: RecipeInterface):
        self.request = request
        self.response = response
        self.recipe_id = recipe_id
        self.config = config
        self.recipe_implementation = recipe_implementation


class EmailVerifyPostOkResponse(APIResponse):
    """
    EmailVerifyPostOkResponse: used to send the ok response if the user
    is successfully verified.
    """

    def __init__(self, user: User):
        self.user = user
        self.status = "OK"

    def to_json(self) -> Dict[str, Any]:
        return {
            'status': self.status,
            'user': {
                'id': self.user.user_id,
                'email': self.user.email
            }
        }


class EmailVerifyPostInvalidTokenErrorResponse(APIResponse):
    """
    EmailVerifyPostInvalidTokenErrorResponse: used to send the error response if the
    user varification fails due to invalid token.
    """

    def __init__(self):
        self.status = "EMAIL_VERIFICATION_INVALID_TOKEN_ERROR"

    def to_json(self) -> Dict[str, Any]:
        return {
            'status': self.status
        }


class IsEmailVerifiedGetOkResponse(APIResponse):
    def __init__(self, is_verified: bool):
        self.status = 'OK'
        self.is_verified = is_verified

    def to_json(self) -> Dict[str, Any]:
        return {
            'status': self.status,
            'isVerified': self.is_verified
        }


class GenerateEmailVerifyTokenPostOkResponse(
        APIResponse):
    def __init__(self):
        self.status = 'OK'
        self.is_email_already_verified_error = False

    def to_json(self) -> Dict[str, Any]:
        return {
            'status': self.status
        }


class GenerateEmailVerifyTokenPostEmailAlreadyVerifiedErrorResponse(
        APIResponse):
    def __init__(self):
        self.status = 'EMAIL_ALREADY_VERIFIED_ERROR'

    def to_json(self) -> Dict[str, Any]:
        return {
            'status': self.status
        }


class APIInterface(ABC):
    def __init__(self):
        self.disable_email_verify_post = False
        self.disable_is_email_verified_get = False
        self.disable_generate_email_verify_token_post = False

    @abstractmethod
    async def email_verify_post(self, token: str, api_options: APIOptions, user_context: Dict[str, Any]) -> Union[EmailVerifyPostOkResponse, EmailVerifyPostInvalidTokenErrorResponse]:
        pass

    @abstractmethod
    async def is_email_verified_get(self, api_options: APIOptions, user_context: Dict[str, Any]) -> IsEmailVerifiedGetOkResponse:
        pass

    @abstractmethod
    async def generate_email_verify_token_post(self, api_options: APIOptions,
                                               user_context: Dict[str, Any]) -> Union[GenerateEmailVerifyTokenPostOkResponse, GenerateEmailVerifyTokenPostEmailAlreadyVerifiedErrorResponse]:
        pass
