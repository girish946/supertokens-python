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

from typing import Any, Dict, List, Union

from .. import interfaces
from ..recipe import ThirdPartyPasswordlessRecipe
from ..types import User


async def create_email_verification_token(user_id: str, user_context: Union[None, Dict[str, Any]] = None):
    """create_email_verification_token.

    Parameters
    ----------
    user_id : str
        user_id
    user_context : Union[None, Dict[str, Any]]
        user_context
    """
    if user_context is None:
        user_context = {}
    email = await ThirdPartyPasswordlessRecipe.get_instance().get_email_for_user_id(user_id, user_context)
    return await ThirdPartyPasswordlessRecipe.get_instance().email_verification_recipe.recipe_implementation.create_email_verification_token(
        user_id, email, user_context)


async def verify_email_using_token(token: str, user_context: Union[None, Dict[str, Any]] = None):
    """verify_email_using_token.

    Parameters
    ----------
    token : str
        token
    user_context : Union[None, Dict[str, Any]]
        user_context
    """
    if user_context is None:
        user_context = {}
    return ThirdPartyPasswordlessRecipe.get_instance().email_verification_recipe.recipe_implementation.verify_email_using_token(
        token, user_context)


async def is_email_verified(user_id: str, user_context: Union[None, Dict[str, Any]] = None):
    """is_email_verified.

    Parameters
    ----------
    user_id : str
        user_id
    user_context : Union[None, Dict[str, Any]]
        user_context
    """
    if user_context is None:
        user_context = {}
    email = await ThirdPartyPasswordlessRecipe.get_instance().get_email_for_user_id(user_id, user_context)
    return await ThirdPartyPasswordlessRecipe.get_instance().email_verification_recipe.recipe_implementation.is_email_verified(
        user_id, email, user_context)


async def unverify_email(user_id: str, user_context: Union[None, Dict[str, Any]] = None):
    """unverify_email.

    Parameters
    ----------
    user_id : str
        user_id
    user_context : Union[None, Dict[str, Any]]
        user_context
    """
    if user_context is None:
        user_context = {}
    email = await ThirdPartyPasswordlessRecipe.get_instance().get_email_for_user_id(user_id, user_context)
    return await ThirdPartyPasswordlessRecipe.get_instance().email_verification_recipe.recipe_implementation.unverify_email(
        user_id, email, user_context)


async def revoke_email_verification_tokens(user_id: str, user_context: Union[None, Dict[str, Any]] = None):
    """revoke_email_verification_tokens.

    Parameters
    ----------
    user_id : str
        user_id
    user_context : Union[None, Dict[str, Any]]
        user_context
    """
    if user_context is None:
        user_context = {}
    email = await ThirdPartyPasswordlessRecipe.get_instance().get_email_for_user_id(user_id, user_context)
    return await ThirdPartyPasswordlessRecipe.get_instance().email_verification_recipe.recipe_implementation.revoke_email_verification_tokens(
        user_id, email, user_context)


async def get_user_by_id(user_id: str, user_context: Union[None, Dict[str, Any]] = None) -> Union[None, User]:
    """get_user_by_id.

    Parameters
    ----------
    user_id : str
        user_id
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    Union[None, User]

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.get_user_by_id(user_id, user_context)


async def get_user_by_third_party_info(third_party_id: str, third_party_user_id: str, user_context: Union[None, Dict[str, Any]] = None):
    """get_user_by_third_party_info.

    Parameters
    ----------
    third_party_id : str
        third_party_id
    third_party_user_id : str
        third_party_user_id
    user_context : Union[None, Dict[str, Any]]
        user_context
    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.get_user_by_thirdparty_info(third_party_id, third_party_user_id, user_context)


async def thirdparty_sign_in_up(third_party_id: str, third_party_user_id: str, email: str, email_verified: bool, user_context: Union[None, Dict[str, Any]] = None):
    """thirdparty_sign_in_up.

    Parameters
    ----------
    third_party_id : str
        third_party_id
    third_party_user_id : str
        third_party_user_id
    email : str
        email
    email_verified : bool
        email_verified
    user_context : Union[None, Dict[str, Any]]
        user_context
    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.thirdparty_sign_in_up(third_party_id, third_party_user_id, email, email_verified, user_context)


async def get_users_by_email(email: str, user_context: Union[None, Dict[str, Any]] = None) -> List[User]:
    """get_users_by_email.

    Parameters
    ----------
    email : str
        email
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    List[User]

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.get_users_by_email(email, user_context)


async def create_code(email: Union[None, str] = None,
                      phone_number: Union[None, str] = None,
                      user_input_code: Union[None, str] = None,
                      user_context: Union[None, Dict[str, Any]] = None) -> interfaces.CreateCodeResult:
    """create_code.

    Parameters
    ----------
    email : Union[None, str]
        email
    phone_number : Union[None, str]
        phone_number
    user_input_code : Union[None, str]
        user_input_code
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    interfaces.CreateCodeResult

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.create_code(email=email, phone_number=phone_number, user_input_code=user_input_code, user_context=user_context)


async def create_new_code_for_device(device_id: str,
                                     user_input_code: Union[str, None] = None,
                                     user_context: Union[None, Dict[str, Any]] = None) -> interfaces.CreateNewCodeForDeviceResult:
    """create_new_code_for_device.

    Parameters
    ----------
    device_id : str
        device_id
    user_input_code : Union[str, None]
        user_input_code
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    interfaces.CreateNewCodeForDeviceResult

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.create_new_code_for_device(device_id=device_id, user_input_code=user_input_code, user_context=user_context)


async def consume_code(pre_auth_session_id: str,
                       user_input_code: Union[str, None] = None,
                       device_id: Union[str, None] = None,
                       link_code: Union[str, None] = None,
                       user_context: Union[None, Dict[str, Any]] = None) -> interfaces.ConsumeCodeResult:
    """consume_code.

    Parameters
    ----------
    pre_auth_session_id : str
        pre_auth_session_id
    user_input_code : Union[str, None]
        user_input_code
    device_id : Union[str, None]
        device_id
    link_code : Union[str, None]
        link_code
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    interfaces.ConsumeCodeResult

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.consume_code(pre_auth_session_id=pre_auth_session_id, user_input_code=user_input_code, device_id=device_id, link_code=link_code, user_context=user_context)


async def get_user_by_phone_number(phone_number: str, user_context: Union[None, Dict[str, Any]] = None) -> Union[User, None]:
    """get_user_by_phone_number.

    Parameters
    ----------
    phone_number : str
        phone_number
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    Union[User, None]

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.get_user_by_phone_number(phone_number=phone_number, user_context=user_context)


async def update_passwordless_user(user_id: str,
                                   email: Union[str, None] = None,
                                   phone_number: Union[str, None] = None,
                                   user_context: Union[None, Dict[str, Any]] = None) -> interfaces.UpdateUserResult:
    """update_passwordless_user.

    Parameters
    ----------
    user_id : str
        user_id
    email : Union[str, None]
        email
    phone_number : Union[str, None]
        phone_number
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    interfaces.UpdateUserResult

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.update_passwordless_user(user_id=user_id, email=email, phone_number=phone_number, user_context=user_context)


async def revoke_all_codes(email: Union[str, None] = None,
                           phone_number: Union[str, None] = None,
                           user_context: Union[None, Dict[str, Any]] = None) -> interfaces.RevokeAllCodesResult:
    """revoke_all_codes.

    Parameters
    ----------
    email : Union[str, None]
        email
    phone_number : Union[str, None]
        phone_number
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    interfaces.RevokeAllCodesResult

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.revoke_all_codes(email=email, phone_number=phone_number, user_context=user_context)


async def revoke_code(code_id: str, user_context: Union[None, Dict[str, Any]] = None) -> interfaces.RevokeCodeResult:
    """revoke_code.

    Parameters
    ----------
    code_id : str
        code_id
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    interfaces.RevokeCodeResult

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.revoke_code(code_id=code_id, user_context=user_context)


async def list_codes_by_email(email: str, user_context: Union[None, Dict[str, Any]] = None) -> List[interfaces.DeviceType]:
    """list_codes_by_email.

    Parameters
    ----------
    email : str
        email
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    List[interfaces.DeviceType]

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.list_codes_by_email(email=email, user_context=user_context)


async def list_codes_by_phone_number(phone_number: str, user_context: Union[None, Dict[str, Any]] = None) -> List[interfaces.DeviceType]:
    """list_codes_by_phone_number.

    Parameters
    ----------
    phone_number : str
        phone_number
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    List[interfaces.DeviceType]

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.list_codes_by_phone_number(phone_number=phone_number, user_context=user_context)


async def list_codes_by_device_id(device_id: str, user_context: Union[None, Dict[str, Any]] = None) -> Union[interfaces.DeviceType, None]:
    """list_codes_by_device_id.

    Parameters
    ----------
    device_id : str
        device_id
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    Union[interfaces.DeviceType, None]

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.list_codes_by_device_id(device_id=device_id, user_context=user_context)


async def list_codes_by_pre_auth_session_id(pre_auth_session_id: str, user_context: Union[None, Dict[str, Any]] = None) -> Union[interfaces.DeviceType, None]:
    """list_codes_by_pre_auth_session_id.

    Parameters
    ----------
    pre_auth_session_id : str
        pre_auth_session_id
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    Union[interfaces.DeviceType, None]

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().recipe_implementation.list_codes_by_pre_auth_session_id(pre_auth_session_id=pre_auth_session_id, user_context=user_context)


async def create_magic_link(email: Union[str, None], phone_number: Union[str, None], user_context: Union[None, Dict[str, Any]] = None) -> str:
    """create_magic_link.

    Parameters
    ----------
    email : Union[str, None]
        email
    phone_number : Union[str, None]
        phone_number
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    str

    """
    if user_context is None:
        user_context = {}
    return await ThirdPartyPasswordlessRecipe.get_instance().passwordless_recipe.create_magic_link(email=email, phone_number=phone_number, user_context=user_context)


async def passwordlessSigninup(email: Union[str, None], phone_number: Union[str, None], user_context: Union[None, Dict[str, Any]] = None) -> interfaces.ConsumeCodeOkResult:
    """passwordlessSigninup.

    Parameters
    ----------
    email : Union[str, None]
        email
    phone_number : Union[str, None]
        phone_number
    user_context : Union[None, Dict[str, Any]]
        user_context

    Returns
    -------
    interfaces.ConsumeCodeOkResult

    """
    if user_context is None:
        user_context = {}
    result = await ThirdPartyPasswordlessRecipe.get_instance().passwordless_recipe.signinup(email=email, phone_number=phone_number, user_context=user_context)

    if result.created_new_user is None or result.user is None:
        raise Exception("Should never come here")
    return interfaces.ConsumeCodeOkResult(result.created_new_user, User(result.user.user_id, result.user.email, result.user.phone_number, None, result.user.time_joined))
