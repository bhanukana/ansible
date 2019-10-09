#!/usr/bin/python

# Copyright 2019 Broadcom. All rights reserved.
# The term 'Broadcom' refers to Broadcom Inc. and/or its subsidiaries.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}


DOCUMENTATION = '''

module: brocade_snmp_system
short_description: Brocade snmp system Configuration
version_added: '2.7'
author: Broadcom BSN Ansible Team <Automation.BSN@broadcom.com>
description:
- Update snmp system configuration

options:

    credential:
        description:
        - login information including
          fos_ip_addr: ip address of the FOS switch
          fos_user_name: login name of FOS switch REST API
          fos_password: password of FOS switch REST API
          https: indicate if HTTPS or HTTP should be used to connect to FOS
        type: dict
        required: true
    vfid:
        description:
        - vfid of the switch to target. The value can be -1 for
          FOS without VF enabled. For VF enabled FOS, a valid vfid
          should be given
        required: false
    throttle:
        description:
        - rest throttling delay in seconds.
        required: false
    snmp_system:
        description:
        - list of snmp system attributes. All writable attributes supported
          by BSN REST API with - replaced with _.
          Some examples are
          - description - description string
        required: true

'''


EXAMPLES = """

  gather_facts: False

  vars:
    credential:
      fos_ip_addr: "{{fos_ip_addr}}"
      fos_user_name: admin
      fos_password: xxxx
      https: False

  tasks:

  - name: initial snmp system configuration
    brocade_snmp_system:
      credential: "{{credential}}"
      vfid: -1
      snmp_system:
        audit_interval: 60
        contact: "Field Support."
        description: "DemoSwitch"
        encryption_enabled: False
        informs_enabled: False
        location: "San Jose"
        security_get_level: 0
        security_set_level: 3
        snmpv1_enabled: True

"""


RETURN = """

msg:
    description: Success message
    returned: success
    type: str

"""


"""
Brocade Fibre Channel snmp system Configuration
"""


from ansible.module_utils.brocade_connection import login, logout, exit_after_login
from ansible.module_utils.brocade_yang import generate_diff
from ansible.module_utils.brocade_snmp import system_patch, system_get, to_human_system, to_fos_system
from ansible.module_utils.basic import AnsibleModule


def main():
    """
    Main function
    """

    argument_spec = dict(
        credential=dict(required=True, type='dict'),
        vfid=dict(required=False, type='int'),
        throttle=dict(required=False, type='float'),
        snmp_system=dict(required=True, type='dict'))

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    input_params = module.params

    # Set up state variables
    fos_ip_addr = input_params['credential']['fos_ip_addr']
    fos_user_name = input_params['credential']['fos_user_name']
    fos_password = input_params['credential']['fos_password']
    https = input_params['credential']['https']
    throttle = input_params['throttle']
    vfid = input_params['vfid']
    snmp_system = input_params['snmp_system']
    result = {"changed": False}

    if vfid is None:
        vfid = 128

    ret_code, auth, fos_version = login(fos_ip_addr,
                           fos_user_name, fos_password,
                           https, throttle, result)
    if ret_code != 0:
        module.exit_json(**result)

    ret_code, response = system_get(fos_user_name, fos_password, fos_ip_addr,
                                     fos_version, https, auth, vfid, result)
    if ret_code != 0:
        exit_after_login(fos_ip_addr, https, auth, result, module)

    resp_system = response["Response"]["system"]

    to_human_system(resp_system)

    diff_attributes = generate_diff(result, resp_system, snmp_system)

    result["diff_attributes"] = diff_attributes
    result["resp_system"] = resp_system
    result["snmp_system"] = snmp_system

    if len(diff_attributes) > 0:
        ret_code = to_fos_system(diff_attributes, result)
        if ret_code != 0:
            exit_after_login(fos_ip_addr, https, auth, result, module)

        if not module.check_mode:
            ret_code = system_patch(fos_user_name, fos_password, fos_ip_addr,
                                     fos_version, https,
                                     auth, vfid, result, diff_attributes)
            if ret_code != 0:
                exit_after_login(fos_ip_addr, https, auth, result, module)

        result["changed"] = True
    else:
        logout(fos_ip_addr, https, auth, result)
        module.exit_json(**result)

    logout(fos_ip_addr, https, auth, result)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
