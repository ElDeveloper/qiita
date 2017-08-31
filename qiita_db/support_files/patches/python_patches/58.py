# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from qiita_db.sql_connection import TRN
from qiita_db.software import Software, Command

with TRN:
    # Retrieve the Qiita plugin
    qiita_plugin = Software.from_name_and_version('Qiita', 'alpha')

    # Create the submit command for VAMPS command
    parameters = {'artifact': ['artifact:["Demultiplexed"]', None]}
    Command.create(qiita_plugin, "submit_to_VAMPS",
                   "submits an artifact to VAMPS", parameters)

    # Create the copy artifact command
    parameters = {'artifact': ['artifact:["Demultiplexed"]', None],
                  'prep_template': ['prep_template', None]}
    Command.create(qiita_plugin, "copy_artifact",
                   "Creates a copy of an artifact", parameters)

    # Create the submit command for EBI command
    parameters = {'artifact': ['artifact:["Demultiplexed"]', None]}
    Command.create(qiita_plugin, "submit_to_EBI",
                   "submits an artifact to EBI", parameters)

    # Create the submit command for delete_artifact
    parameters = {'artifact': ['artifact:["Demultiplexed"]', None]}
    Command.create(qiita_plugin, "delete_artifact",
                   "Delete an artifact", parameters)

    # Create the submit command for create a sample template
    parameters = {'artifact': ['artifact:["Demultiplexed"]', None]}
    Command.create(qiita_plugin, "create_sample_template",
                   "Create a sample template", parameters)
