# -*- coding: utf-8 -*-
'''
Configuration of netadapter on windows with hyperv
===============================================

This module provides the ``hyperv_netadapter`` state on Windows hosts.

Below is an example of the configuration for a physical interface:

.. code-block:: yaml

    vnic0:
        hyper_netadapter.managed:
            - mac: <mac>
            - name: <name>

'''

from __future__ import absolute_import

import salt.utils

import logging
log = logging.getLogger(__name__)

__virtualname__ = 'hyperv_netadapter'


def __virtual__():
    '''
    State load only if it on windows server
    '''
    if salt.utils.is_windows():
        return __virtualname__
    return False


def managed(mac, name=None, **kwargs):
    '''
    Ensure that the netadapter named by mac is configured properly.

    mac
        @MAC address of the physical netadapter

    name
        Name of the netadapter

    '''
    ret = {'name': mac,
           'changes': {},
           'comment': '',
           'result': False}

    netadapter = None
    try:
        for card in __salt__['hyperv.netadapters']():
            if card['mac'] == mac:
                if netadapter is not None:
                    raise Exception*(
                        'duplicate netadapter found for macaddress %s' % (mac,))
                netadapter = card
        if netadapter is None:
            raise Exception(
                'netadapter with %s macaddress was not found' % (mac,))
    except Exception, e:
        ret['comment'] = str(e)
        ret['result'] = False
    else:
        if name is not None:  # manage the netadapter name
            if not name == netadapter['name']:
                ret['changes']['name'] = {'new': name,
                                          'old': netadapter['name']}
        try:
            __salt__['hyperv.set_netadapter'](mac, name=name)
        except Exception, e:
            ret['comment'] = str(e)
            ret['result'] = False
        else:
            ret['comment'] = 'Netadapter properties are up to date'
            ret['result'] = True

    return ret


if __name__ == "__main__":
    __salt__ = ''
    __opts__ = ''

    import sys
    sys.exit(0)
