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


if __name__ == "__main__":
    __salt__ = ''

    import sys
    sys.exit(0)
