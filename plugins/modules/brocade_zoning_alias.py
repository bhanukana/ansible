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

module: brocade_zoning_alias
short_description: Brocade Zoning Alias
version_added: '2.7'
author: Broadcom BSN Ansible Team <Automation.BSN@broadcom.com>
description:
- Create, detroy, or update Aliases. The whole of aliases and
  aliases_to_delete are applied to FOS within a single login session
  to termininate after the completion


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
    aliases:
        description:
        - List of aliases to be created or modified. If an alias does
          not exist in the current Zone Database, the alias will be
          created with the members specified. If an alias already
          exist in the current Zone Database, the alias is upcated to
          reflect to members specificed. In other word, new members
          will be added and removed members will be removed.
          If no aliases_to_delete are listed, aliases is required.
          aliases_to_delete and aliases are mutually exclusive.
        required: false
    aliases_to_delete:
        description:
        - List of aliases to be deleted. If no aliases are listed,
          aliases_to_delete is required.  aliases_to_delete and
          aliases are mutually exclusive.
        required: false

'''


EXAMPLES = """

  gather_facts: False

  vars:
    credential:
      fos_ip_addr: "{{fos_ip_addr}}"
      fos_user_name: admin
      fos_password: fibranne
      https: False
    aliases:
      - name: Host1
        members:
          - 11:22:33:44:55:66:77:88
      - name: Target1
        members:
          - 22:22:33:44:55:66:77:99      
      - name: Target2
        members:
          - 22:22:33:44:55:66:77:aa
      - name: Target3
        members:
          - 22:22:33:44:55:66:77:bb
    aliases_to_delete:
      - name: Target1
      - name: Target2
      - name: Target3

  tasks:

  - name: Create aliases
    brocade_zoning_alias:
      credential: "{{credential}}"
      vfid: -1
      aliases: "{{aliases}}"
#      aliases_to_delete: "{{aliases_to_delete}}"

"""


RETURN = """

msg:
    description: Success message
    returned: success
    type: str

"""


"""
Brocade Zoning Alias
"""


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.brocade_connection import login, logout, exit_after_login
from ansible.module_utils.brocade_zoning import zoning_common, alias_post, alias_delete, alias_get,\
    process_member_diff


def alias_process_diff(result, aliases, c_aliases):
    """
    return the diff from expected aliases vs. current aliases

    :param aliases: list of expected aliases
    :type aliases: list
    :param c_aliases: list of current aliases
    :type c_aliases: list
    :return: indicate if diff or the same
    :rtype: bool
    :return: list of aliases with to be added members
    :rtype: list
    :return: list of aliases with to be removed members
    :rtype: list
    """
    post_aliases = []
    remove_aliases = []
    for alias in aliases:
        found_in_c = False
        for c_alias in c_aliases:
            if alias["name"] == c_alias["alias-name"]:
                found_in_c = True
                added_members, removed_members = process_member_diff(
                    result, alias["members"],
                    c_alias["member-entry"]["alias-entry-name"])

                if len(added_members) > 0:
                    post_alias = {}
                    post_alias["name"] = alias["name"]
                    post_alias["members"] = added_members
                    post_aliases.append(post_alias)
                if len(removed_members) > 0:
                    remove_alias = {}
                    remove_alias["name"] = alias["name"]
                    remove_alias["members"] = removed_members
                    remove_aliases.append(remove_alias)
                continue
        if not found_in_c:
            post_aliases.append(alias)

    return 0, post_aliases, remove_aliases


def main():
    """
    Main function
    """

    argument_spec = dict(
        credential=dict(required=True, type='dict'),
        vfid=dict(required=False, type='int'),
        throttle=dict(required=False, type='float'),
        aliases=dict(required=False, type='list'),
        aliases_to_delete=dict(required=False, type='list'))

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
    aliases = input_params['aliases']
    aliases_to_delete = input_params['aliases_to_delete']
    result = {"changed": False}

    if vfid is None:
        vfid = 128

    ret_code, auth, fos_version = login(fos_ip_addr,
                           fos_user_name, fos_password,
                           https, throttle, result)
    if ret_code != 0:
        module.exit_json(**result)

    zoning_common(fos_ip_addr, https, auth, vfid, result, module, aliases,
                  aliases_to_delete, "alias",
                  alias_process_diff, alias_get, alias_post, alias_delete,
                  None)

    ret_code = logout(fos_ip_addr, https, auth, result)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
