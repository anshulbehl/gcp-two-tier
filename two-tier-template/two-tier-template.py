# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

"""Creates the Compute Engine."""
#Variables
randstr = uuid.uuid4().hex[:6].lower()
zone = "us-central1-a"
region = "us-central1"
sshkey = "admin:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC6VfvLtgxxVgKdRLSgJBewzxNB4xKFSHInnekC2FxVQ8bpqSd1/30nLsXPc1r/NLPMFEU4H5KZuizz7cLYpfn//oPfOpInK5L71GoYb6P/vs+7bg+UcH/nETKjXS4RW9VSfJK4CefI4C9DZETikIdQjQH7H87gu3xP/KH6Kb2QwLMHQGtgfv8ps5vh27VE9hBW+F/p3K/D+5KfUE1PaJEAHfe1d52Op3f3+O2EXIk5P4aNde4+i4rUr8o8QDGohi5YkumlEmjSw3w5b7yqxw0aBNS5jGB+yAKJlln4DDEpJUsosbUOgy2qwMrwiH2cqUgQygYOwc0ov4MEtIh9dtCH admin"
bootstrap_bucket = "2tier-bootstrap"
scripts_bucket = "2tier-bootstap"
serviceaccount = "service-account@p-64cslcy0bvfp-0.iam.gserviceaccount.com"


image = "vmseries-flex-byol-1000"
mgmt_network = "mgmt-network"
mgmt_subnet = "mgmt-subnet"
web_network = "web-network"
web_subnet = "web-subnet"
untrust_network = "untrust-network"
untrust_subnet = "untrust-subnet"
imageWeb = "rhel-8"
machineType = "n1-standard-4"
machineTypeWeb = "f1-micro"
fwname = "vm-series"
webserver_name = "web-vm"
mgmt_firewall_rule = "mgmt-firewall"
untrust_firewall_rule = "untrust-firewall"
web_firewall_rule = "web-firewall-rule"
web_route = "web-route"


def GenerateConfig(unused_context):
  """Creates the Compute Engine with multiple templates."""
  resources = [
  {
      'name': fwname,
      'type': 'vm-series-template.py',
      'properties': {
          'name': fwname,
          'zone': zone,
          'machineType': machineType,
          'mgmt-network': mgmt_network,
          'mgmt-subnet': mgmt_subnet,
          'web-network': web_network,
          'web-subnet': web_subnet,
          'untrust-network': untrust_network,
          'untrust-subnet': untrust_subnet,
          'image': image,
          'bootstrapbucket': bootstrap_bucket,
          'sshkey': sshkey,
          'serviceaccount': serviceaccount
      }
  },
  {
      'name': webserver_name,
      'type': 'webserver-template.py',
      'properties': {
          'name': webserver_name,
          'zone': zone,
          'machineTypeWeb': machineTypeWeb,
          'web-network': web_network,
          'web-subnet': web_subnet,
          'imageWeb': imageWeb,
          'sshkey': sshkey,
          'serviceaccount': serviceaccount,
          'bootstrapbucket': scripts_bucket,
      }
  },
  {
      'name': mgmt_network,
      'type': 'network-template.py'
  },
  {
      'name': mgmt_subnet,
      'type': 'subnetwork-template.py',
      'properties': {
          'network': mgmt_network,
          'ipcidrrange': '10.5.0.0/24',
          'region': region
      }
  },
  {
      'name': web_network,
      'type': 'network-template.py'
  },
  {
      'name': web_subnet,
      'type': 'subnetwork-template.py',
      'properties': {
          'network': web_network,
          'ipcidrrange': '10.5.2.0/24',
          'region': region
      }
  },
  {
      'name': untrust_network,
      'type': 'network-template.py'
  },
  {
      'name': untrust_subnet,
      'type': 'subnetwork-template.py',
      'properties': {
          'network': untrust_network,
          'ipcidrrange': '10.5.1.0/24',
          'region': region
      }
  },
  {
      'metadata': {
        'dependsOn': [mgmt_network, web_network, untrust_network]
      },      
      'name': web_route,
      'type': 'compute.v1.route',
      'properties': {
        'priority': 100,
        'network': '$(ref.'+web_network+'.selfLink)',
        'destRange': '0.0.0.0/0',
        'nextHopIp': '$(ref.vm-series.networkInterfaces[2].networkIP)'
      }
  },
  {
      'metadata': {
        'dependsOn': [mgmt_network, web_network, untrust_network]
      },
      'name': mgmt_firewall_rule,
      'type': 'compute.v1.firewall',
      'properties': {
          'region': region, 
          'network': '$(ref.'+mgmt_network+'.selfLink)',
          'direction': 'INGRESS',
          'priority': 1000,
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
            'IPProtocol': 'tcp',
            'ports': [22, 443]
          }]
      }
  },
  {
      'metadata': {
        'dependsOn': [mgmt_network, web_network, untrust_network]
      },
      'name': untrust_firewall_rule,
      'type': 'compute.v1.firewall',
      'properties': {
          'region': region, 
          'network': '$(ref.'+untrust_network+'.selfLink)',
          'direction': 'INGRESS',
          'priority': 1000,
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
            'IPProtocol': 'tcp',
            'ports': [80, 221, 222]
          }]
      }
  },
  {
      'metadata': {
        'dependsOn': [mgmt_network, web_network, untrust_network]
      },
      'name': web_firewall_rule,
      'type': 'compute.v1.firewall',
      'properties': {
          'region': region, 
        'network': '$(ref.'+web_network+'.selfLink)',
          'direction': 'INGRESS',
          'priority': 1000,
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
            'IPProtocol': 'tcp',
            },{
            'IPProtocol': 'udp',
            },{
            'IPProtocol': 'icmp'
          }]
      }
  },
  ]

  return {'resources': resources}
