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

"""category manager taxonomies delete command."""


from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.category_manager import delete_lib


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Delete(base.Command):
  """Delete a category taxonomy."""

  @staticmethod
  def Args(parser):
    """Register flags for this command."""
    parser.add_argument('id',
                        default='',
                        metavar='TAXONOMY_ID',
                        help='Id of the taxonomy to be deleted.')

  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
      command invocation.

    Returns:
      Status of command execution.
    """
    return delete_lib.DeleteTaxonomy(args.id)
