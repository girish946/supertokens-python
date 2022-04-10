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
from typing import List, Union

from supertokens_python import Supertokens
from supertokens_python.types import UsersResponse


async def get_users_oldest_first(limit: Union[int, None] = None, pagination_token: Union[str, None] = None,
                                 include_recipe_ids: Union[None, List[str]] = None) -> UsersResponse:
    """get_users_oldest_first.

    Parameters
    ----------
    limit : Union[int, None]
        limit
    pagination_token : Union[str, None]
        pagination_token
    include_recipe_ids : Union[None, List[str]]
        include_recipe_ids

    Returns
    -------
    UsersResponse

    """
    return await Supertokens.get_instance().get_users('ASC', limit, pagination_token, include_recipe_ids)


async def get_users_newest_first(limit: Union[int, None] = None, pagination_token: Union[str, None] = None,
                                 include_recipe_ids: Union[None, List[str]] = None) -> UsersResponse:
    """get_users_newest_first.

    Parameters
    ----------
    limit : Union[int, None]
        limit
    pagination_token : Union[str, None]
        pagination_token
    include_recipe_ids : Union[None, List[str]]
        include_recipe_ids

    Returns
    -------
    UsersResponse

    """
    return await Supertokens.get_instance().get_users('DESC', limit, pagination_token, include_recipe_ids)


async def get_user_count(include_recipe_ids: Union[None, List[str]] = None) -> int:
    """get_user_count.

    Parameters
    ----------
    include_recipe_ids : Union[None, List[str]]
        include_recipe_ids

    Returns
    -------
    int

    """
    return await Supertokens.get_instance().get_user_count(include_recipe_ids)


async def delete_user(user_id: str) -> None:
    """delete_user.

    Parameters
    ----------
    user_id : str
        user_id

    Returns
    -------
    None

    """
    return await Supertokens.get_instance().delete_user(user_id)
