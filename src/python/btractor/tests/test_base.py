#-*-coding:utf-8-*-
"""
@package btractor.tests
@brief tests for btractor

@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
from __future__ import unicode_literals
__all__ = []

from .base import TractorTestCase

from btractor.delegates import NukeTractorDelegate


class TestDelegates(TractorTestCase):
    """Tests for delegates of all kinds"""
    __slots__ = ()
        
    def test_nuke_delegate(self):
        """Test delegate log parsing capabilities"""
        logfile = self.fixture_path("nuke_readerror.log")
        assert logfile.isfile()
        
        delegate = NukeTractorDelegate()
        exit_status_seen_count = 0
        for line in open(logfile):
            res, value = delegate._classifiy_line(line.strip())
            exit_status_seen_count += res == NukeTractorDelegate.LINE_FATAL
        # end for each line
        assert exit_status_seen_count == 3, "should have parsed the status exactly three times"
# end class TestDelegates
