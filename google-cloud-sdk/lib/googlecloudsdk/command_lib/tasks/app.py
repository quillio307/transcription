# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utilities for App Engine apps for `gcloud tasks` commands."""

from googlecloudsdk.api_lib.app import appengine_api_client as app_engine_api
from googlecloudsdk.api_lib.app import exceptions as app_api_exceptions
from googlecloudsdk.calliope import base as calliope_base
from googlecloudsdk.command_lib.app import create_util
from googlecloudsdk.command_lib.tasks import constants
from googlecloudsdk.core import exceptions
from googlecloudsdk.core import properties
from googlecloudsdk.core.console import console_io


_MORE_REGIONS_AVAILABLE_WARNING = """\
The regions listed here are only those in which the Cloud Tasks API is
available. To see full list of App Engine regions available,
create an app using the following command:

    $ gcloud app create
"""


class RegionResolvingError(exceptions.Error):
  """Error for when the app's region cannot be ultimately determined."""


def ResolveAppLocation():
  """Determines region of the App Engine app in the project or creates an app.

  Returns:
    The existing or created app's locationId.

  Raises:
    RegionResolvingError: If the region of the app could not be determined.
  """
  app_engine_api_client = app_engine_api.GetApiClientForTrack(
      calliope_base.ReleaseTrack.GA)
  app = _GetApp(app_engine_api_client) or _CreateApp(app_engine_api_client)
  if app is not None:
    region = constants.CLOUD_MULTIREGION_TO_REGION_MAP.get(app.locationId,
                                                           app.locationId)
    return region
  raise RegionResolvingError(
      'Could not determine the region of the project\'s App Engine app. '
      'Please try again.')


def _GetApp(app_engine_api_client):
  try:
    return app_engine_api_client.GetApplication()
  except app_api_exceptions.NotFoundError:
    return None


def _CreateApp(app_engine_api_client):
  """Walks the user through creating an AppEngine app."""
  project = properties.VALUES.core.project.GetOrFail()
  if console_io.PromptContinue(
      message=('There is no App Engine app in project [{}].'.format(project)),
      prompt_string=('Would you like to create one'),
      throw_if_unattended=True):
    try:
      create_util.CreateAppInteractively(
          app_engine_api_client, project, regions=constants.VALID_REGIONS,
          extra_warning=_MORE_REGIONS_AVAILABLE_WARNING)
    except create_util.AppAlreadyExistsError:
      raise create_util.AppAlreadyExistsError(
          'App already exists in project [{}]. This may be due a race '
          'condition. Please try again.'.format(project))
    else:
      return _GetApp(app_engine_api_client)
  return None
