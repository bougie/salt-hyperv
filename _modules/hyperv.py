# -*- coding: utf-8 -*-
'''
Support for Windows HyperV
'''

from __future__ import absolute_import

import json
import logging
import salt.utils
from salt.exceptions import CommandExecutionError, SaltInvocationError

log = logging.getLogger(__name__)

__virtualname__ = 'hyperv'

_SWITCH_TYPES = {
    0: 'external',
    1: 'internal',
    2: 'private'}


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
            cmd = "%s | ConvertTo-Json -Depth 1 -Compress" % (cmd,)
        ret = __salt__['cmd.run_all'](cmd,
                                      shell='powershell',
                                      python_shell=False)
        if ret['retcode'] == 0:
            if json_output:
                if len(ret['stdout'].strip()) == 0:
                    # create an empty list if nothing is returned
                    ret['stdout'] = "[]"
                ret['stdout'] = json.loads(ret['stdout'])
                if not isinstance(ret['stdout'], list):
                    # if only one object is returned, append it to a list
                    ret['stdout'] = [ret['stdout']]
            return ret['stdout']
        else:
            raise CommandExecutionError(str(ret))


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


def add_vswitch(name, switchtype, **kwargs):
    '''
    Create a new vswitch

    CLI Example:

    .. code-block:: bash

        salt '*' hyperv.add_vswitch <name> private|internal
        salt '*' hyperv.add_vswitch <name> external interface=<interface>
    '''
    cmd = 'New-VMSwitch'
    if name is not None and len(name.strip()) > 0:
        cmd = '%s -Name %s' % (cmd, name)

        if switchtype is not None and len(switchtype.strip()) > 0:
            if switchtype not in _SWITCH_TYPES.values():
                raise SaltInvocationError(
                    'switchtype %s not supported' % (switchtype,))

            # external switch
            if switchtype == _SWITCH_TYPES[0]:
                if 'interface' not in kwargs:
                    raise SaltInvocationError(
                        'no interface name specified for external vswitch')
                cmd = '%s -NetAdapterName %s' % (cmd, kwargs['interface'])
            # internal or private switch
            elif switchtype in [_SWITCH_TYPES[1], _SWITCH_TYPES[2]]:
                cmd = '%s -SwitchType %s' % (cmd, switchtype)

            try:
                _psrun(cmd)
            except:
                return False
            else:
                return True
        else:
            raise SaltInvocationError('vswitch type not specified')
    else:
        raise SaltInvocationError('vswitch name not specified')


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
