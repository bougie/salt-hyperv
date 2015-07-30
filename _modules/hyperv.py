# -*- coding: utf-8 -*-
'''
Support for Windows HyperV
'''

from __future__ import absolute_import

import json
import logging
import salt.utils
# from salt.exceptions import CommandExecutionError, SaltInvocationError

log = logging.getLogger(__name__)

__virtualname__ = 'hyperv'


def __virtual__():
    '''
    Module load only if it on windows server
    '''
    if salt.utils.is_windows():
        return __virtualname__
    return False


def _has_powershell():
    '''
    Confirm if Powershell is available
    '''
    return 'powershell' in __salt__['cmd.run'](['where', 'powershell'],
                                               python_shell=False)


def _psrun(cmd, json_output=True):
    '''
    Run a powershell command
    '''

    if _has_powershell():
        if json_output:
            cmd = "%s | ConvertTo-Json" % (cmd,)
        ret = __salt__['cmd.run'](cmd, shell='powershell', python_shell=False)
        if json_output:
            ret = json.loads(ret)
        return ret


def install(with_gui=False):
    pass


def vswitchs(**kwargs):
    '''
    Return a list of dictionary of information about all vSwitch on the minion

    CLI Example:

    .. code-block:: bash

        salt '*' hyperv.vswitchs
    '''
    switchs = []
    for switch in _psrun('Get-VMSwitch'):
        switchs.append({'name': switch['Name'],
                        'computername': switch['ComputerName'],
                        'type': switch['SwitchType'],
                        'netadapter': switch['NetAdapterInterfaceDescription']})
    return switchs


def add_vswitch(**kwargs):
    pass


def remove_vswitch(**kwargs):
    pass


def netadapters(all=False, **kwargs):
    '''
    Return a list of dictionary of physical network adapters

    all
        show all network adapters (included virtual one created by Hyper-V)

    CLI Example:

    .. code-block:: bash

        salt '*' hyperv.netadapters
        salt '*' hyperv.netadapters all=True
    '''
    args = ''
    if all is False:
        args = ' -Physical'

    adapters = []
    for adapter in _psrun('Get-NetAdapter%s' % (args,)):
        adapters.append({
            'name': adapter['Name'],
            'description': adapter['InterfaceDescription'],
            'mac': adapter['MacAddress']
        })
    return adapters


def vms(**kwargs):
    '''
    Return a list of dictionary of virtual machines

    CLI Example:

    .. code-block:: bash

        salt '*' hyperv.vms
    '''
    vms = []
    for vm in _psrun('Get-VM'):
        vms.append({
            'name': vm['Name'],
            'state': vm['State']})
    return vms


if __name__ == "__main__":
    __salt__ = ''

    import sys
    sys.exit(0)
