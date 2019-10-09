# Copyright 2019 Broadcom. All rights reserved.
# The term 'Broadcom' refers to Broadcom Inc. and/or its subsidiaries.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.brocade_url import url_get_to_dict, url_patch, HTTP, HTTPS, url_patch_single_object, url_post, url_delete
from ansible.module_utils.brocade_yang import yang_to_human, human_to_yang
from ansible.module_utils.brocade_ssh import ssh_and_configure

__metaclass__ = type


"""
Brocade logging utils
"""


REST_IPFILTER_RULE = "/rest/running/brocade-security/ipfilter-rule"
REST_IPFILTER_POLICY = "/rest/running/brocade-security/ipfilter-policy"
REST_USER_CONFIG = "/rest/running/brocade-security/user-config"


def to_human_ipfilter_rule(attributes):
    for k, v in attributes.items():
        if v == "true":
            attributes[k] = True
        elif v == "false":
            attributes[k] = False

    yang_to_human(attributes)

def to_fos_ipfilter_rule(attributes, result):
    human_to_yang(attributes)

    for k, v in attributes.items():
        if isinstance(v, bool):
            if v == True:
                attributes[k] = "true"
            else:
                attributes[k] = "false"

    return 0


def ipfilter_rule_get(fos_ip_addr, is_https, auth, vfid, result):
    """
        retrieve existing ipfilter rule configuration 

        :param fos_ip_addr: ip address of FOS switch
        :type fos_ip_addr: str
        :param is_https: indicate to use HTTP or HTTPS
        :type is_https: bool
        :param auth: authorization struct from login
        :type struct: dict
        :param result: dict to keep track of execution msgs
        :type result: dict
        :return: code to indicate failure or success
        :rtype: int
        :return: dict of ipfilter rule configurations
        :rtype: dict
    """
    full_url = (HTTPS if is_https else HTTP) +\
        fos_ip_addr + REST_IPFILTER_RULE

    return (url_get_to_dict(fos_ip_addr, is_https, auth, vfid,
                              result, full_url))

def ipfilter_rule_xml_str(result, rules):
    xml_str = ""

    for rule in rules:
        xml_str = xml_str + "<ipfilter-rule>"

        xml_str = xml_str + "<policy-name>" + rule["policy-name"] + "</policy-name>"
        xml_str = xml_str + "<index>" + str(rule["index"]) + "</index>"

        for k, v in rule.items():
            if k != "policy-name" and k != "index":
                k = k.replace("_", "-")
                xml_str = xml_str + "<" + k + ">" +\
                    str(v) + "</" + k + ">"

        xml_str = xml_str + "</ipfilter-rule>"

    return xml_str


def ipfilter_rule_patch(fos_ip_addr, is_https, auth,
                       vfid, result, rules):
    """
        update existing ip filter configurations

        :param fos_ip_addr: ip address of FOS switch
        :type fos_ip_addr: str
        :param is_https: indicate to use HTTP or HTTPS
        :type is_https: bool
        :param auth: authorization struct from login
        :type struct: dict
        :param result: dict to keep track of execution msgs
        :type result: dict
        :param diff_attributes: list of attributes for update
        :type ports: dict
        :return: code to indicate failure or success
        :rtype: int
        :return: list of dict of chassis configurations
        :rtype: list
    """
    full_url = (HTTPS if is_https else HTTP) +\
        fos_ip_addr + REST_IPFILTER_RULE

    xml_str = ipfilter_rule_xml_str(result, rules)

    result["patch_ipfilter_str"] = xml_str

    return url_patch(fos_ip_addr, is_https, auth, vfid, result,
                     full_url, xml_str)


def ipfilter_rule_post(fos_ip_addr, is_https, auth,
                       vfid, result, rules):
    """
        add to ipfilter rule configurations

        :param fos_ip_addr: ip address of FOS switch
        :type fos_ip_addr: str
        :param is_https: indicate to use HTTP or HTTPS
        :type is_https: bool
        :param auth: authorization struct from login
        :type struct: dict
        :param result: dict to keep track of execution msgs
        :type result: dict
        :param diff_attributes: list of attributes for update
        :type ports: dict
        :return: code to indicate failure or success
        :rtype: int
        :return: list of dict of chassis configurations
        :rtype: list
    """
    full_url = (HTTPS if is_https else HTTP) +\
        fos_ip_addr + REST_IPFILTER_RULE

    xml_str = ipfilter_rule_xml_str(result, rules)

    result["post_ipfilter_str"] = xml_str

    return url_post(fos_ip_addr, is_https, auth, vfid, result,
                     full_url, xml_str)


def ipfilter_rule_delete(fos_ip_addr, is_https, auth,
                       vfid, result, rules):
    """
        delete existing ipfilter rule configurations

        :param fos_ip_addr: ip address of FOS switch
        :type fos_ip_addr: str
        :param is_https: indicate to use HTTP or HTTPS
        :type is_https: bool
        :param auth: authorization struct from login
        :type struct: dict
        :param result: dict to keep track of execution msgs
        :type result: dict
        :param diff_attributes: list of attributes for update
        :type ports: dict
        :return: code to indicate failure or success
        :rtype: int
        :return: list of dict of chassis configurations
        :rtype: list
    """
    full_url = (HTTPS if is_https else HTTP) +\
        fos_ip_addr + REST_IPFILTER_RULE

    xml_str = ipfilter_rule_xml_str(result, rules)

    result["delete_ipfilter_str"] = xml_str

    return url_delete(fos_ip_addr, is_https, auth, vfid, result,
                     full_url, xml_str)


def to_human_ipfilter_policy(attributes):
    for k, v in attributes.items():
        if v == "true":
            attributes[k] = True
        elif v == "false":
            attributes[k] = False

    yang_to_human(attributes)

def to_fos_ipfilter_policy(attributes, result):
    human_to_yang(attributes)

    for k, v in attributes.items():
        if isinstance(v, bool):
            if v == True:
                attributes[k] = "true"
            else:
                attributes[k] = "false"

    return 0


def ipfilter_policy_get(fos_ip_addr, is_https, auth, vfid, result):
    """
        retrieve existing ipfilter policy configuration 

        :param fos_ip_addr: ip address of FOS switch
        :type fos_ip_addr: str
        :param is_https: indicate to use HTTP or HTTPS
        :type is_https: bool
        :param auth: authorization struct from login
        :type struct: dict
        :param result: dict to keep track of execution msgs
        :type result: dict
        :return: code to indicate failure or success
        :rtype: int
        :return: dict of ipfilter policy configurations
        :rtype: dict
    """
    full_url = (HTTPS if is_https else HTTP) +\
        fos_ip_addr + REST_IPFILTER_POLICY

    return (url_get_to_dict(fos_ip_addr, is_https, auth, vfid,
                              result, full_url))


def ipfilter_policy_xml_str(result, rules):
    xml_str = ""

    for rule in rules:
        xml_str = xml_str + "<ipfilter-policy>"

        xml_str = xml_str + "<name>" + rule["name"] + "</name>"

        for k, v in rule.items():
            if k != "name":
                k = k.replace("_", "-")
                xml_str = xml_str + "<" + k + ">" +\
                    str(v) + "</" + k + ">"

        xml_str = xml_str + "</ipfilter-policy>"

    return xml_str


def ipfilter_policy_patch(fos_ip_addr, is_https, auth,
                       vfid, result, policies):
    """
        update existing ip filter configurations

        :param fos_ip_addr: ip address of FOS switch
        :type fos_ip_addr: str
        :param is_https: indicate to use HTTP or HTTPS
        :type is_https: bool
        :param auth: authorization struct from login
        :type struct: dict
        :param result: dict to keep track of execution msgs
        :type result: dict
        :param diff_attributes: list of attributes for update
        :type ports: dict
        :return: code to indicate failure or success
        :rtype: int
        :return: list of dict of chassis configurations
        :rtype: list
    """
    full_url = (HTTPS if is_https else HTTP) +\
        fos_ip_addr + REST_IPFILTER_POLICY

    xml_str = ipfilter_policy_xml_str(result, policies)

    result["patch_ipfilter_policy_str"] = xml_str

    return url_patch(fos_ip_addr, is_https, auth, vfid, result,
                     full_url, xml_str)


def ipfilter_policy_post(fos_ip_addr, is_https, auth,
                       vfid, result, policies):
    """
        add to ipfilter policy configurations

        :param fos_ip_addr: ip address of FOS switch
        :type fos_ip_addr: str
        :param is_https: indicate to use HTTP or HTTPS
        :type is_https: bool
        :param auth: authorization struct from login
        :type struct: dict
        :param result: dict to keep track of execution msgs
        :type result: dict
        :param diff_attributes: list of attributes for update
        :type ports: dict
        :return: code to indicate failure or success
        :rtype: int
        :return: list of dict of chassis configurations
        :rtype: list
    """
    full_url = (HTTPS if is_https else HTTP) +\
        fos_ip_addr + REST_IPFILTER_POLICY

    xml_str = ipfilter_policy_xml_str(result, policies)

    result["post_ipfilter_policy_str"] = xml_str

    return url_post(fos_ip_addr, is_https, auth, vfid, result,
                     full_url, xml_str)


def ipfilter_policy_delete(fos_ip_addr, is_https, auth,
                       vfid, result, policies):
    """
        delete existing ipfilter policy configurations

        :param fos_ip_addr: ip address of FOS switch
        :type fos_ip_addr: str
        :param is_https: indicate to use HTTP or HTTPS
        :type is_https: bool
        :param auth: authorization struct from login
        :type struct: dict
        :param result: dict to keep track of execution msgs
        :type result: dict
        :param diff_attributes: list of attributes for update
        :type ports: dict
        :return: code to indicate failure or success
        :rtype: int
        :return: list of dict of chassis configurations
        :rtype: list
    """
    full_url = (HTTPS if is_https else HTTP) +\
        fos_ip_addr + REST_IPFILTER_POLICY

    xml_str = ipfilter_policy_xml_str(result, policies)

    result["delete_ipfilter_policy_str"] = xml_str

    return url_delete(fos_ip_addr, is_https, auth, vfid, result,
                     full_url, xml_str)



def to_human_user_config(attributes):
    for k, v in attributes.items():
        if v == "true":
            attributes[k] = True
        elif v == "false":
            attributes[k] = False

    yang_to_human(attributes)

def to_fos_user_config(attributes, result):
    human_to_yang(attributes)

    for k, v in attributes.items():
        if isinstance(v, bool):
            if v == True:
                attributes[k] = "true"
            else:
                attributes[k] = "false"

    return 0


def user_config_get(fos_ip_addr, is_https, auth, vfid, result):
    """
        retrieve existing user config configuration 

        :param fos_ip_addr: ip address of FOS switch
        :type fos_ip_addr: str
        :param is_https: indicate to use HTTP or HTTPS
        :type is_https: bool
        :param auth: authorization struct from login
        :type struct: dict
        :param result: dict to keep track of execution msgs
        :type result: dict
        :return: code to indicate failure or success
        :rtype: int
        :return: dict of ipfilter policy configurations
        :rtype: dict
    """
    full_url = (HTTPS if is_https else HTTP) +\
        fos_ip_addr + REST_USER_CONFIG

    return (url_get_to_dict(fos_ip_addr, is_https, auth, vfid,
                              result, full_url))


def user_config_xml_str(result, users):
    xml_str = ""

    for user in users:
        xml_str = xml_str + "<user-config>"

        xml_str = xml_str + "<name>" + user["name"] + "</name>"

        for k, v in user.items():
            if k != "name":
                if isinstance(v, list):
                    xml_str = xml_str + "<" + k + ">"
                    for entry in v:
                        for k1, v1 in entry.items():
                            xml_str = xml_str + "<" + k1 + ">" +\
                                str(v1) + "</" + k1 + ">"
                    xml_str = xml_str + "</" + k + ">"
                else:
                    xml_str = xml_str + "<" + k + ">" +\
                        str(v) + "</" + k + ">"

        xml_str = xml_str + "</user-config>"

    return xml_str


def user_config_patch(login, password, fos_ip_addr, fos_version, is_https, auth,
                       vfid, result, users):
    """
        update existing user config configurations

        :param fos_ip_addr: ip address of FOS switch
        :type fos_ip_addr: str
        :param is_https: indicate to use HTTP or HTTPS
        :type is_https: bool
        :param auth: authorization struct from login
        :type struct: dict
        :param result: dict to keep track of execution msgs
        :type result: dict
        :param diff_attributes: list of attributes for update
        :type ports: dict
        :return: code to indicate failure or success
        :rtype: int
        :return: list of dict of chassis configurations
        :rtype: list
    """
    l_users = users[:]

    if fos_version < "v9.0":
        # walk through all the users and check for account-enabled
        # if pre 9.0 since the attribute patch is not supported pre 
        for l_user in l_users:
            if "account-enabled" in l_user:
                if l_user["account-enabled"] == "true":
                    rssh, sshstr = ssh_and_configure(login, password, fos_ip_addr, False, "userconfig --change " + l_user["name"] + " -e yes" , "")
                    if rssh != 0:
                        result["failed"] = True
                        result["msg"] = "Failed to enable account"
                    else:
                        result["changed"] = True
                        result["messages"] = "account enabled"
                elif l_user["account-enabled"] == "false":
                    rssh, sshstr = ssh_and_configure(login, password, fos_ip_addr, False, "userconfig --change " + l_user["name"] + " -e no" , "")
                    if rssh != 0:
                        result["failed"] = True
                        result["msg"] = "Failed to disable account"
                    else:
                        result["changed"] = True
                        result["messages"] = "account disabled"
                else:
                    result["failed"] = True
                    result["msg"] = "unknown account-enabled value. Invalid input"
                l_user.pop("account-enabled")

        rest_users = []
        for l_user in l_users:
            if len(l_user) > 1:
                rest_users.append(l_user)

    if len(rest_users) == 0:
        return 0

    full_url = (HTTPS if is_https else HTTP) +\
        fos_ip_addr + REST_USER_CONFIG

    xml_str = user_config_xml_str(result, rest_users)

    result["patch_user_config_str"] = xml_str

    return url_patch(fos_ip_addr, is_https, auth, vfid, result,
                     full_url, xml_str)


def user_config_post(fos_ip_addr, is_https, auth,
                       vfid, result, users):
    """
        add to ipfilter policy configurations

        :param fos_ip_addr: ip address of FOS switch
        :type fos_ip_addr: str
        :param is_https: indicate to use HTTP or HTTPS
        :type is_https: bool
        :param auth: authorization struct from login
        :type struct: dict
        :param result: dict to keep track of execution msgs
        :type result: dict
        :param diff_attributes: list of attributes for update
        :type ports: dict
        :return: code to indicate failure or success
        :rtype: int
        :return: list of dict of chassis configurations
        :rtype: list
    """
    full_url = (HTTPS if is_https else HTTP) +\
        fos_ip_addr + REST_USER_CONFIG

    xml_str = user_config_xml_str(result, users)

    result["post_user_config_str"] = xml_str

    return url_post(fos_ip_addr, is_https, auth, vfid, result,
                     full_url, xml_str)


def user_config_delete(fos_ip_addr, is_https, auth,
                       vfid, result, users):
    """
        delete existing user config configurations

        :param fos_ip_addr: ip address of FOS switch
        :type fos_ip_addr: str
        :param is_https: indicate to use HTTP or HTTPS
        :type is_https: bool
        :param auth: authorization struct from login
        :type struct: dict
        :param result: dict to keep track of execution msgs
        :type result: dict
        :param diff_attributes: list of attributes for update
        :type ports: dict
        :return: code to indicate failure or success
        :rtype: int
        :return: list of dict of chassis configurations
        :rtype: list
    """
    full_url = (HTTPS if is_https else HTTP) +\
        fos_ip_addr + REST_USER_CONFIG

    xml_str = user_config_xml_str(result, users)

    result["delete_user_config_str"] = xml_str

    return url_delete(fos_ip_addr, is_https, auth, vfid, result,
                     full_url, xml_str)


