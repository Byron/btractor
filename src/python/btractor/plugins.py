#-*-coding:utf-8-*-
"""
@package btractor.plugins
@brief Implements interfaces in btractor.interfaces

@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
from __future__ import unicode_literals
__all__ = ['TractorProcessDataProvider', 'TractorNodeGeneratorChainProvider']

import os

import bapp
from .interfaces import (ITractorProcessDataProvider,
                         ITractorNodeGeneratorChainProvider )
from .alf.generators import TractorCmdGeneratorBase
from .alf.generators import NodeGeneratorChainBase
from bkvstore import KeyValueStoreProvider


class TractorProcessDataProvider(ITractorProcessDataProvider, bapp.plugin_type()):
    """Implements the data provider interface, works together with TractorDelegateMixin and TractorCmdGeneratorBase"""
    __slots__ = ()
    
    def data(self):
        evar = TractorCmdGeneratorBase.data_storage_env_var
        if evar not in os.environ:
            return None
        return TractorCmdGeneratorBase.deserialize_data(os.environ[evar])
        
    def set_progress(self, progress):
        print "TR_PROGRESS %03i%%"
        
    def as_kvstore(self):
        data = self.data()
        if data is None:
            return None
        return KeyValueStoreProvider(data)

# end class TractorProcessDataProvider


class TractorNodeGeneratorChainProvider(ITractorNodeGeneratorChainProvider, bapp.plugin_type()):
    """Provide nodes of the required type using services"""
    __slots__ = ()

    def chains(self):
        return bapp.main().context().new_instance(NodeGeneratorChainBase)

# end class TractorNodeGeneratorChainProvider

