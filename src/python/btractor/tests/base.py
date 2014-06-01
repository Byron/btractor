#-*-coding:utf-8-*-
"""
@package btractor.tests.base
@brief Base classes and utilities for tractor tests

@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
from __future__ import unicode_literals
__all__ = ['TractorTestCase']


from butility.tests import TestCase



# ==============================================================================
## @name Classes
# ------------------------------------------------------------------------------
## @{

class TractorTestCase(TestCase):
    """A test case with some maya utilities"""
    __slots__ = ()

    ## Subdirectory to the ./fixtures root
    fixture_subdir = 'processing/tractor'

# end class TractorTestCase

## -- End Classes -- @}



