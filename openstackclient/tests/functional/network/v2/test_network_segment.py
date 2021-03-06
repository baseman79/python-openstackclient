#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import uuid

from openstackclient.tests.functional.network.v2 import common


class NetworkSegmentTests(common.NetworkTests):
    """Functional tests for network segment"""

    def setUp(self):
        super(NetworkSegmentTests, self).setUp()
        # Nothing in this class works with Nova Network
        if not self.haz_network:
            self.skipTest("No Network service present")

        self.NETWORK_NAME = uuid.uuid4().hex
        self.PHYSICAL_NETWORK_NAME = uuid.uuid4().hex

        # Create a network for the segment
        opts = self.get_opts(['id'])
        raw_output = self.openstack(
            'network create ' + self.NETWORK_NAME + opts
        )
        self.addCleanup(self.openstack,
                        'network delete ' + self.NETWORK_NAME)
        self.NETWORK_ID = raw_output.strip('\n')

        # Get the segment for the network.
        opts = self.get_opts(['ID', 'Network'])
        raw_output = self.openstack(
            'network segment list '
            '--network ' + self.NETWORK_NAME + ' ' +
            opts
        )
        raw_output_row = raw_output.split('\n')[0]
        self.NETWORK_SEGMENT_ID = raw_output_row.split(' ')[0]

    def test_network_segment_create_delete(self):
        opts = self.get_opts(['id'])
        raw_output = self.openstack(
            ' network segment create --network ' + self.NETWORK_ID +
            ' --network-type geneve ' +
            ' --segment 2055 test_segment ' + opts
        )
        network_segment_id = raw_output.strip('\n')
        raw_output = self.openstack('network segment delete ' +
                                    network_segment_id)
        self.assertOutput('', raw_output)

    def test_network_segment_list(self):
        opts = self.get_opts(['ID'])
        raw_output = self.openstack('network segment list' + opts)
        self.assertIn(self.NETWORK_SEGMENT_ID, raw_output)

    def test_network_segment_set(self):
        new_description = 'new_description'
        raw_output = self.openstack('network segment set ' +
                                    '--description ' + new_description +
                                    ' ' + self.NETWORK_SEGMENT_ID)
        self.assertOutput('', raw_output)
        opts = self.get_opts(['description'])
        raw_output = self.openstack('network segment show ' +
                                    self.NETWORK_SEGMENT_ID + opts)
        self.assertEqual(new_description + "\n", raw_output)

    def test_network_segment_show(self):
        opts = self.get_opts(['network_id'])
        raw_output = self.openstack('network segment show ' +
                                    self.NETWORK_SEGMENT_ID + opts)
        self.assertEqual(self.NETWORK_ID + "\n", raw_output)
