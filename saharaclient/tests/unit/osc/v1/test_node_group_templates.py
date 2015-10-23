# Copyright (c) 2015 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from openstackclient.tests import utils as osc_utils

from saharaclient.api import node_group_templates as api_ngt
from saharaclient.osc.v1 import node_group_templates as osc_ngt
from saharaclient.tests.unit.osc.v1 import fakes


NGT_INFO = {
    "node_processes": [
        "namenode",
        "tasktracker"
    ],
    "name": "template",
    "tenant_id": "tenant_id",
    "availability_zone": 'av_zone',
    "use_autoconfig": True,
    "hadoop_version": "0.1",
    "shares": None,
    "is_default": False,
    "description": 'description',
    "node_configs": {},
    "is_proxy_gateway": False,
    "auto_security_group": True,
    "volume_type": None,
    "volumes_size": 2,
    "volume_mount_prefix": "/volumes/disk",
    "plugin_name": "fake",
    "is_protected": False,
    "security_groups": None,
    "floating_ip_pool": "floating_pool",
    "is_public": True,
    "id": "ea3c8624-a1f0-49cf-83c4-f5a6634699ca",
    "flavor_id": "2",
    "volumes_availability_zone": None,
    "volumes_per_node": 2,
    "volume_local_to_instance": False
}


class TestNodeGroupTemplates(fakes.TestDataProcessing):
    def setUp(self):
        super(TestNodeGroupTemplates, self).setUp()
        self.ngt_mock = (
            self.app.client_manager.data_processing.node_group_templates)
        self.ngt_mock.reset_mock()


class TestCreateNodeGroupTemplate(TestNodeGroupTemplates):
    # TODO(apavlov): check for creation with --json
    def setUp(self):
        super(TestCreateNodeGroupTemplate, self).setUp()
        self.ngt_mock.create.return_value = api_ngt.NodeGroupTemplate(
            None, NGT_INFO)

        # Command to test
        self.cmd = osc_ngt.CreateNodeGroupTemplate(self.app, None)

    def test_ngt_create_minimum_options(self):
        arglist = ['--name', 'template', '--plugin', 'fake', '--version',
                   '0.1', '--processes', 'namenode', 'tasktracker']
        verifylist = [('name', 'template'), ('plugin', 'fake'),
                      ('version', '0.1'),
                      ('processes', ['namenode', 'tasktracker'])]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        # Check that correct arguments were passed
        self.ngt_mock.create.assert_called_once_with(
            auto_security_group=False, availability_zone=None,
            description=None, flavor_id=None, floating_ip_pool=None,
            hadoop_version='0.1', is_protected=False, is_proxy_gateway=False,
            is_public=False, name='template',
            node_processes=['namenode', 'tasktracker'], plugin_name='fake',
            security_groups=None, use_autoconfig=False,
            volume_local_to_instance=False,
            volume_type=None, volumes_availability_zone=None,
            volumes_per_node=None, volumes_size=None, shares=None,
            node_configs=None)

    def test_ngt_create_all_options(self):
        arglist = ['--name', 'template', '--plugin', 'fake', '--version',
                   '0.1', '--processes', 'namenode', 'tasktracker',
                   '--security-groups', 'secgr', '--auto-security-group',
                   '--availability-zone', 'av_zone', '--flavor', '2',
                   '--floating-ip-pool', 'floating_pool', '--volumes-per-node',
                   '2', '--volumes-size', '2', '--volumes-type', 'type',
                   '--volumes-availability-zone', 'vavzone',
                   '--volumes-mount-prefix', '/volume/asd',
                   '--volumes-locality', '--description', 'descr',
                   '--autoconfig', '--proxy-gateway', '--public',
                   '--protected']

        verifylist = [('name', 'template'), ('plugin', 'fake'),
                      ('version', '0.1'),
                      ('processes', ['namenode', 'tasktracker']),
                      ('security_groups', ['secgr']),
                      ('auto_security_group', True),
                      ('availability_zone', 'av_zone'), ('flavor', '2'),
                      ('floating_ip_pool', 'floating_pool'),
                      ('volumes_per_node', 2), ('volumes_size', 2),
                      ('volumes_type', 'type'),
                      ('volumes_availability_zone', 'vavzone'),
                      ('volumes_mount_prefix', '/volume/asd'),
                      ('volumes_locality', True), ('description', 'descr'),
                      ('autoconfig', True), ('proxy_gateway', True),
                      ('public', True), ('protected', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that correct arguments were passed
        self.ngt_mock.create.assert_called_once_with(
            auto_security_group=True, availability_zone='av_zone',
            description='descr', flavor_id='2',
            floating_ip_pool='floating_pool', hadoop_version='0.1',
            is_protected=True, is_proxy_gateway=True, is_public=True,
            name='template', node_processes=['namenode', 'tasktracker'],
            plugin_name='fake', security_groups=['secgr'], use_autoconfig=True,
            volume_local_to_instance=True, volume_type='type',
            volumes_availability_zone='vavzone', volumes_per_node=2,
            volumes_size=2, shares=None, node_configs=None)

        # Check that columns are correct
        expected_columns = (
            'Auto security group', 'Availability zone', 'Description',
            'Flavor id', 'Floating ip pool', 'Id', 'Is default',
            'Is protected', 'Is proxy gateway', 'Is public', 'Name',
            'Node processes', 'Plugin name', 'Security groups',
            'Use autoconfig', 'Version', 'Volume local to instance',
            'Volume mount prefix', 'Volume type', 'Volumes availability zone',
            'Volumes per node', 'Volumes size')
        self.assertEqual(expected_columns, columns)

        # Check that data is correct
        expected_data = (
            True, 'av_zone', 'description', '2', 'floating_pool',
            'ea3c8624-a1f0-49cf-83c4-f5a6634699ca', False, False, False,
            True, 'template', 'namenode, tasktracker', 'fake', None, True,
            '0.1', False, '/volumes/disk', None, None, 2, 2)
        self.assertEqual(expected_data, data)


class TestListNodeGroupTemplates(TestNodeGroupTemplates):
    def setUp(self):
        super(TestListNodeGroupTemplates, self).setUp()
        self.ngt_mock.list.return_value = [api_ngt.NodeGroupTemplate(
            None, NGT_INFO)]

        # Command to test
        self.cmd = osc_ngt.ListNodeGroupTemplates(self.app, None)

    def test_ngt_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that columns are correct
        expected_columns = ['Name', 'Id', 'Plugin name', 'Version']
        self.assertEqual(expected_columns, columns)

        # Check that data is correct
        expected_data = [('template', 'ea3c8624-a1f0-49cf-83c4-f5a6634699ca',
                          'fake', '0.1')]
        self.assertEqual(expected_data, list(data))

    def test_ngt_list_long(self):
        arglist = ['--long']
        verifylist = [('long', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that columns are correct
        expected_columns = ['Name', 'Id', 'Plugin name', 'Version',
                            'Node processes', 'Description']
        self.assertEqual(expected_columns, columns)

        # Check that data is correct
        expected_data = [('template', 'ea3c8624-a1f0-49cf-83c4-f5a6634699ca',
                          'fake', '0.1', 'namenode, tasktracker',
                          'description')]
        self.assertEqual(expected_data, list(data))

    def test_ngt_list_extra_search_opts(self):
        arglist = ['--plugin', 'fake', '--version', '0.1', '--name', 'templ']
        verifylist = [('plugin', 'fake'), ('version', '0.1'),
                      ('name', 'templ')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that columns are correct
        expected_columns = ['Name', 'Id', 'Plugin name', 'Version']
        self.assertEqual(expected_columns, columns)

        # Check that data is correct
        expected_data = [('template', 'ea3c8624-a1f0-49cf-83c4-f5a6634699ca',
                          'fake', '0.1')]
        self.assertEqual(expected_data, list(data))


class TestShowNodeGroupTemplate(TestNodeGroupTemplates):
    def setUp(self):
        super(TestShowNodeGroupTemplate, self).setUp()
        self.ngt_mock.find_unique.return_value = api_ngt.NodeGroupTemplate(
            None, NGT_INFO)

        # Command to test
        self.cmd = osc_ngt.ShowNodeGroupTemplate(self.app, None)

    def test_ngt_show(self):
        arglist = ['template']
        verifylist = [('node_group_template', 'template')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that correct arguments were passed
        self.ngt_mock.find_unique.assert_called_once_with(name='template')

        # Check that columns are correct
        expected_columns = (
            'Auto security group', 'Availability zone', 'Description',
            'Flavor id', 'Floating ip pool', 'Id', 'Is default',
            'Is protected', 'Is proxy gateway', 'Is public', 'Name',
            'Node processes', 'Plugin name', 'Security groups',
            'Use autoconfig', 'Version', 'Volume local to instance',
            'Volume mount prefix', 'Volume type', 'Volumes availability zone',
            'Volumes per node', 'Volumes size')
        self.assertEqual(expected_columns, columns)

        # Check that data is correct
        expected_data = (
            True, 'av_zone', 'description', '2', 'floating_pool',
            'ea3c8624-a1f0-49cf-83c4-f5a6634699ca', False, False, False,
            True, 'template', 'namenode, tasktracker', 'fake', None, True,
            '0.1', False, '/volumes/disk', None, None, 2, 2)
        self.assertEqual(expected_data, data)


class TestDeleteNodeGroupTemplate(TestNodeGroupTemplates):
    def setUp(self):
        super(TestDeleteNodeGroupTemplate, self).setUp()
        self.ngt_mock.find_unique.return_value = api_ngt.NodeGroupTemplate(
            None, NGT_INFO)

        # Command to test
        self.cmd = osc_ngt.DeleteNodeGroupTemplate(self.app, None)

    def test_ngt_delete(self):
        arglist = ['template']
        verifylist = [('node_group_template', ['template'])]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        # Check that correct arguments were passed
        self.ngt_mock.delete.assert_called_once_with(
            'ea3c8624-a1f0-49cf-83c4-f5a6634699ca')


class TestUpdateNodeGroupTemplate(TestNodeGroupTemplates):
    # TODO(apavlov): check for update with --json
    def setUp(self):
        super(TestUpdateNodeGroupTemplate, self).setUp()
        self.ngt_mock.find_unique.return_value = api_ngt.NodeGroupTemplate(
            None, NGT_INFO)
        self.ngt_mock.update.return_value = api_ngt.NodeGroupTemplate(
            None, NGT_INFO)

        # Command to test
        self.cmd = osc_ngt.UpdateNodeGroupTemplate(self.app, None)

    def test_ngt_update_no_options(self):
        arglist = []
        verifylist = []

        self.assertRaises(osc_utils.ParserException, self.check_parser,
                          self.cmd, arglist, verifylist)

    def test_ngt_update_all_options(self):
        arglist = ['template', '--name', 'template', '--plugin', 'fake',
                   '--version', '0.1', '--processes', 'namenode',
                   'tasktracker', '--security-groups', 'secgr',
                   '--auto-security-group-enable',
                   '--availability-zone', 'av_zone', '--flavor', '2',
                   '--floating-ip-pool', 'floating_pool', '--volumes-per-node',
                   '2', '--volumes-size', '2', '--volumes-type', 'type',
                   '--volumes-availability-zone', 'vavzone',
                   '--volumes-mount-prefix', '/volume/asd',
                   '--volumes-locality-enable', '--description', 'descr',
                   '--autoconfig-enable', '--proxy-gateway-enable', '--public',
                   '--protected']

        verifylist = [('node_group_template', 'template'),
                      ('name', 'template'), ('plugin', 'fake'),
                      ('version', '0.1'),
                      ('processes', ['namenode', 'tasktracker']),
                      ('security_groups', ['secgr']),
                      ('use_auto_security_group', True),
                      ('availability_zone', 'av_zone'), ('flavor', '2'),
                      ('floating_ip_pool', 'floating_pool'),
                      ('volumes_per_node', 2), ('volumes_size', 2),
                      ('volumes_type', 'type'),
                      ('volumes_availability_zone', 'vavzone'),
                      ('volumes_mount_prefix', '/volume/asd'),
                      ('volume_locality', True),
                      ('description', 'descr'), ('use_autoconfig', True),
                      ('is_proxy_gateway', True),
                      ('is_public', True), ('is_protected', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that correct arguments were passed
        self.ngt_mock.update.assert_called_once_with(
            'ea3c8624-a1f0-49cf-83c4-f5a6634699ca',
            auto_security_group=True, availability_zone='av_zone',
            description='descr', flavor_id='2',
            floating_ip_pool='floating_pool', hadoop_version='0.1',
            is_protected=True, is_proxy_gateway=True, is_public=True,
            name='template', node_processes=['namenode', 'tasktracker'],
            plugin_name='fake', security_groups=['secgr'], use_autoconfig=True,
            volume_local_to_instance=True, volume_type='type',
            volumes_availability_zone='vavzone', volumes_per_node=2,
            volumes_size=2, shares=None, node_configs=None)

        # Check that columns are correct
        expected_columns = (
            'Auto security group', 'Availability zone', 'Description',
            'Flavor id', 'Floating ip pool', 'Id', 'Is default',
            'Is protected', 'Is proxy gateway', 'Is public', 'Name',
            'Node processes', 'Plugin name', 'Security groups',
            'Use autoconfig', 'Version', 'Volume local to instance',
            'Volume mount prefix', 'Volume type', 'Volumes availability zone',
            'Volumes per node', 'Volumes size')
        self.assertEqual(expected_columns, columns)

        # Check that data is correct
        expected_data = (
            True, 'av_zone', 'description', '2', 'floating_pool',
            'ea3c8624-a1f0-49cf-83c4-f5a6634699ca', False, False, False,
            True, 'template', 'namenode, tasktracker', 'fake', None, True,
            '0.1', False, '/volumes/disk', None, None, 2, 2)
        self.assertEqual(expected_data, data)