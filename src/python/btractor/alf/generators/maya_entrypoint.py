#-*-coding:utf-8-*-
"""
@package btractor.alf.generators.maya_entrypoint
@brief Startup whatever tractor provded to us

@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
from __future__ import unicode_literals
__all__ = []

import logging
log = logging.getLogger('btractor.alf.generators.maya_entrypoint')

import bapp

from btractor import ITractorProcessDataProvider
from .maya import MayaBatchTaskGenerator


# ==============================================================================
## @name Utilities
# ------------------------------------------------------------------------------
## @{

def run():
    """run the tractor-provided script"""
    provider = bapp.main().context().new_instance(ITractorProcessDataProvider)
    store = provider.as_kvstore()
    assert store is not None, "Must be executed via tractor and receive contextual data - don't now what to run"
    
    data = store.value(MayaBatchTaskGenerator.static_field_schema.key(), MayaBatchTaskGenerator.static_field_schema)
    
    # The evaluated string has access to our data and store
    ######################
    log.info(data.cmd.python)
    exec(data.cmd.python)
    ######################
    
## -- End Utilities -- @}

