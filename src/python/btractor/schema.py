#-*-coding:utf-8-*-
"""
@package btractor.schema
@brief tractor-related schemas for general use

@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
from __future__ import unicode_literals
from butility.future import str

__all__ = ['submitter_schema']

from bkvstore import KeyValueStoreSchema

tractor_schema = KeyValueStoreSchema('tractor', { 'submission' : { 'priority' : dict( low = 0,
                                                                                         normal = 1,
                                                                                         high = 2 ) 
                                                                    },
                                                    'engine' :     { 'hostname' : str,
                                                                     'port' : int
                                                                   }
                                                   }
                                       )
