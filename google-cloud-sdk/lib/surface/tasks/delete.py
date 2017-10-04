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
"""`gcloud tasks delete` command."""

from googlecloudsdk.api_lib.tasks import tasks
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.tasks import parsers
from googlecloudsdk.core import log


class Delete(base.DeleteCommand):
  """Delete a task from a queue."""

  @staticmethod
  def Args(parser):
    parsers.AddTaskResourceArgs(parser, 'to delete')

  def Run(self, args):
    tasks_client = tasks.Tasks()
    task_ref = parsers.ParseTask(args.task, args.queue)
    tasks_client.Delete(task_ref)
    log.DeletedResource(task_ref.Name(), kind='task')
