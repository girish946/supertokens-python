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

from typing import TYPE_CHECKING, Callable, Union

if TYPE_CHECKING:
    from .interfaces import RecipeInterface, APIInterface
    from supertokens_python import AppInfo
    from supertokens_python.recipe.jwt import OverrideConfig as JWTOverrideConfig

from supertokens_python.normalised_url_domain import NormalisedURLDomain
from supertokens_python.normalised_url_path import NormalisedURLPath


class InputOverrideConfig:
    """InputOverrideConfig.
    """

    def __init__(self, functions: Union[Callable[[RecipeInterface], RecipeInterface], None] = None,
                 apis: Union[Callable[[APIInterface],
                                      APIInterface], None] = None,
                 jwt_feature: Union[JWTOverrideConfig, None] = None):
        """__init__.

        Parameters
        ----------
        functions : Union[Callable[[RecipeInterface], RecipeInterface], None]
            functions
        apis : Union[Callable[[APIInterface],
                                              APIInterface], None]
            apis
        jwt_feature : Union[JWTOverrideConfig, None]
            jwt_feature
        """
        self.functions = functions
        self.apis = apis
        self.jwt_feature = jwt_feature


class OverrideConfig:
    """OverrideConfig.
    """

    def __init__(self, functions: Union[Callable[[RecipeInterface], RecipeInterface],
                                        None] = None, apis: Union[Callable[[APIInterface], APIInterface], None] = None):
        """__init__.

        Parameters
        ----------
        functions : Union[Callable[[RecipeInterface], RecipeInterface],
                                                None]
            functions
        apis : Union[Callable[[APIInterface], APIInterface], None]
            apis
        """
        self.functions = functions
        self.apis = apis


class OpenIdConfig:
    """OpenIdConfig.
    """

    def __init__(self, override: OverrideConfig,
                 issuer_domain: NormalisedURLDomain, issuer_path: NormalisedURLPath):
        """__init__.

        Parameters
        ----------
        override : OverrideConfig
            override
        issuer_domain : NormalisedURLDomain
            issuer_domain
        issuer_path : NormalisedURLPath
            issuer_path
        """
        self.override = override
        self.issuer_domain = issuer_domain
        self.issuer_path = issuer_path


def validate_and_normalise_user_input(
        app_info: AppInfo,
        issuer: Union[str, None] = None,
        override: Union[InputOverrideConfig, None] = None):
    """validate_and_normalise_user_input.

    Parameters
    ----------
    app_info : AppInfo
        app_info
    issuer : Union[str, None]
        issuer
    override : Union[InputOverrideConfig, None]
        override
    """
    if issuer is None:
        issuer_domain = app_info.api_domain
        issuer_path = app_info.api_base_path
    else:
        issuer_domain = NormalisedURLDomain(issuer)
        issuer_path = NormalisedURLPath(issuer)

    if not issuer_path.equals(app_info.api_base_path):
        raise Exception(
            'The path of the issuer URL must be equal to the apiBasePath. The default value is /auth')

    if override is None:
        override = InputOverrideConfig()

    return OpenIdConfig(OverrideConfig(
        functions=override.functions, apis=override.apis), issuer_domain, issuer_path)
