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

from typing import Any, Dict, Union

from supertokens_python.recipe.emailpassword.interfaces import (
    CreateResetPasswordResult, RecipeInterface, ResetPasswordUsingTokenResult,
    SignInResult, SignUpResult, UpdateEmailOrPasswordResult)
from supertokens_python.recipe.emailpassword.types import User
from supertokens_python.recipe.thirdpartyemailpassword.interfaces import \
    RecipeInterface as ThirdPartyEmailPasswordRecipeInterface


class RecipeImplementation(RecipeInterface):
    """RecipeImplementation.
    """

    def __init__(
            self, recipe_implementation: ThirdPartyEmailPasswordRecipeInterface):
        """__init__.

        Parameters
        ----------
        recipe_implementation : ThirdPartyEmailPasswordRecipeInterface
            recipe_implementation
        """
        super().__init__()
        self.recipe_implementation = recipe_implementation

    async def get_user_by_id(self, user_id: str, user_context: Dict[str, Any]) -> Union[User, None]:
        """get_user_by_id.

        Parameters
        ----------
        user_id : str
            user_id
        user_context : Dict[str, Any]
            user_context

        Returns
        -------
        Union[User, None]

        """
        user = await self.recipe_implementation.get_user_by_id(user_id, user_context)

        if user is None or user.third_party_info is not None:
            return None

        return User(user_id=user.user_id, email=user.email, time_joined=user.time_joined)

    async def get_user_by_email(self, email: str, user_context: Dict[str, Any]) -> Union[User, None]:
        """get_user_by_email.

        Parameters
        ----------
        email : str
            email
        user_context : Dict[str, Any]
            user_context

        Returns
        -------
        Union[User, None]

        """
        users = await self.recipe_implementation.get_users_by_email(email, user_context)

        for user in users:
            if user.third_party_info is None:
                return User(user_id=user.user_id, email=user.email, time_joined=user.time_joined)

        return None

    async def create_reset_password_token(self, user_id: str, user_context: Dict[str, Any]) -> CreateResetPasswordResult:
        """create_reset_password_token.

        Parameters
        ----------
        user_id : str
            user_id
        user_context : Dict[str, Any]
            user_context

        Returns
        -------
        CreateResetPasswordResult

        """
        return await self.recipe_implementation.create_reset_password_token(user_id, user_context)

    async def reset_password_using_token(self, token: str, new_password: str, user_context: Dict[str, Any]) -> ResetPasswordUsingTokenResult:
        """reset_password_using_token.

        Parameters
        ----------
        token : str
            token
        new_password : str
            new_password
        user_context : Dict[str, Any]
            user_context

        Returns
        -------
        ResetPasswordUsingTokenResult

        """
        return await self.recipe_implementation.reset_password_using_token(token, new_password, user_context)

    async def sign_in(self, email: str, password: str, user_context: Dict[str, Any]) -> SignInResult:
        """sign_in.

        Parameters
        ----------
        email : str
            email
        password : str
            password
        user_context : Dict[str, Any]
            user_context

        Returns
        -------
        SignInResult

        """
        return await self.recipe_implementation.emailpassword_sign_in(email, password, user_context)

    async def sign_up(self, email: str, password: str, user_context: Dict[str, Any]) -> SignUpResult:
        """sign_up.

        Parameters
        ----------
        email : str
            email
        password : str
            password
        user_context : Dict[str, Any]
            user_context

        Returns
        -------
        SignUpResult

        """
        return await self.recipe_implementation.emailpassword_sign_up(email, password, user_context)

    async def update_email_or_password(self, user_id: str, email: Union[str, None],
                                       password: Union[str, None], user_context: Dict[str, Any]) -> UpdateEmailOrPasswordResult:
        """update_email_or_password.

        Parameters
        ----------
        user_id : str
            user_id
        email : Union[str, None]
            email
        password : Union[str, None]
            password
        user_context : Dict[str, Any]
            user_context

        Returns
        -------
        UpdateEmailOrPasswordResult

        """
        return await self.recipe_implementation.update_email_or_password(user_id, email, password, user_context)
