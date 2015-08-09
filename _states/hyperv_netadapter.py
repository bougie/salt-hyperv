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


def managed(tgt, **kwargs):
    '''
    Ensure that the netadapter named by mac is configured properly.

    tgt
        target / filter use to identify the netadapter by an unique key.
        target have to be formated with the following format:
            <filter_name:<filter_value>
        allowed format are:
            - mac

    '''
    ret = {'name': tgt,
           'changes': {},
           'comment': '',
           'result': False}

    netadapter = None
    try:
        tgt_type = tgt.split(':')[0]
        tgt = ':'.join(tgt.split(':')[1:])

        for card in __salt__['hyperv.netadapters']():
            if tgt_type == 'mac' and card['mac'] == tgt:
                if netadapter is not None:
                    raise Exception(
                        'duplicate netadapter found for filter %s/%s' % (
                            tgt,
                            tgt_type,))
                netadapter = card
        else:
            raise Exception('no netadapter found on host')
        if netadapter is None:
            raise Exception('no netadapter found for filter %s/%s' % (
                tgt,
                tgt_type,))
    except Exception, e:
        ret['comment'] = str(e)
        ret['result'] = False
    else:
        args = None
        if 'name' in kwargs:  # manage the netadapter name
            if not kwargs['name'] == netadapter['name']:
                ret['changes']['name'] = {'new': kwargs['name'],
                                          'old': netadapter['name']}
                args = {'name': kwargs['name']}

        if args is not None:
            try:
                __salt__['hyperv.set_netadapter'](tgt, tgt_type, **args)
            except Exception, e:
                ret['comment'] = str(e)
                ret['result'] = False
            else:
                ret['comment'] = 'Netadapter properties are now up to date'
                ret['result'] = True
        else:
            ret['comment'] = 'Netadapter properties are already up to date'
            ret['result'] = True

    return ret


if __name__ == "__main__":
    __salt__ = ''
    __opts__ = ''

    import sys
    sys.exit(0)
