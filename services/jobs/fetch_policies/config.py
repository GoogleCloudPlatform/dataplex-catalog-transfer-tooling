# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module to manage application configuration settings based on command-line
inputs. Utilizes `common.utils` for argument parsing.
"""

from argparse import ArgumentParser, Action as argparseAction
from typing import Dict, Any
import re
from common.utils import parse_common_args


class ValidateScope(argparseAction):
    """
    Validates scope format and extracts type and ID.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        pattern = r"^(organizations|folder)/(\d+)$"
        match = re.match(pattern, values)

        if match:
            scope_type = match.group(1).rstrip("s")
            scope_id = match.group(2)
        else:
            parser.error(
                "Invalid scope format. Expected 'organizations/{orgID}' "
                "or 'folder/{folderID}'."
            )

        setattr(
            namespace,
            self.dest,
            {"scope_type": scope_type.upper(), "scope_id": scope_id},
        )


class ParseChoiceWithBoth(argparseAction):
    """
    Parses choices, allowing 'both' to represent all options.
    """

    _transform = None

    def __init__(self, *args, **kwargs):
        if "transform_function" in kwargs:
            self._transform = kwargs["transform_function"]
            del kwargs["transform_function"]
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if "both" == values:
            actual_value = list(self.choices)
            actual_value.remove("both")
        else:
            actual_value = [values]
        if self._transform is not None:
            actual_value = [self._transform(val) for val in actual_value]
        setattr(namespace, self.dest, actual_value)


def create_parse_choice_with_both(transform_function: callable):
    def inner(*args, **kwargs):
        return ParseChoiceWithBoth(
            transform_function=transform_function, *args, **kwargs
        )

    return inner


def parse_service_args(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-s",
        "--scope",
        type=str,
        required=True,
        action=ValidateScope,
        help=(
            "Should be formatted as organizations/{orgId} or folder/{folderId},"
            " defining the scope of projects for the process."
        ),
    )
    parser.add_argument(
        "-rt",
        "--resource-types",
        type=str,
        choices=["entry_group", "tag_template", "both"],
        default=["entry_group", "tag_template"],
        action=ParseChoiceWithBoth,
        help=(
            "Resources to fetch IAM policies for: entry_group, tag_template, "
            "or both. (default: both)."
        ),
    )
    parser.add_argument(
        "-ms",
        "--managing-systems",
        type=str,
        choices=["data_catalog", "dataplex", "both"],
        default=["DATA_CATALOG", "DATAPLEX"],
        action=create_parse_choice_with_both(lambda option: option.upper()),
        help=(
            "System from which IAM policies should be fetched: "
            "DATA_CATALOG, DATAPLEX, or BOTH. (default: both)."
        ),
    )
    parser.add_argument(
        "-l",
        "--service-location",
        type=str,
        default="us-central1",
        help=(
            "The location/region where the job is running. "
            "(default: 'us-central1')."
        ),
    )
    parser.add_argument(
        "-q",
        "--queue",
        default="iam-discovery",
        type=str,
        help=(
            "The name of the queue to use for projects discovery "
            "(default: 'iam-discovery')."
        ),
    )
    parser.add_argument(
        "-hn",
        "--handler-name",
        default="fetch-policies-handler",
        type=str,
        help=(
            "The name of the handler responsible for processing projects "
            "(default: 'fetch-policies-handler')."
        ),
    )


def get_application_config() -> Dict[str, Any]:
    """
    Combines common and service-specific arguments into a unified configuration.
    """
    parser = ArgumentParser(description="CLI for find fetch policies job")

    parse_service_args(parser)
    parse_common_args(parser)

    args = parser.parse_args()

    if args.dataset_name is None:
        args.dataset_name = (
            "transfer_tooling_dry_run" if args.dry_run else "transfer_tooling"
        )

    return {
        "scope": args.scope,
        "resource_types": args.resource_types,
        "managing_systems": args.managing_systems,
        "project_name": args.project,
        "dataset_name": args.dataset_name,
        "service_location": args.service_location,
        "queue": args.queue,
        "handler_name": args.handler_name,
        "dataset_location": args.dataset_location,
    }
