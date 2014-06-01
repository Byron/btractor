#-*-coding:utf-8-*-
"""
@package btractor.submission.plugins.bash
@brief Implements a chain for bash-batching, but it can possibly be used for anything

@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
from __future__ import unicode_literals
__all__ = ['BashTaskChain', 'ChunkedBashTaskChain']

import bapp
from ...alf.generators import (NodeGeneratorChain,
                               FrameSequenceGenerator,
                               BashExecuteTaskGenerator )

class BashTaskChain(NodeGeneratorChain, bapp.plugin_type()):
    """Simple bash batch commands, for now without chunking."""
    __slots__ = ()
    
    def __init__(self):
        """Setup chain"""
        super(BashTaskChain, self).__init__()
        self.set_head(BashExecuteTaskGenerator())
        
    _plugin_name = "Bash Execution"

# end class MayaBatchTaskChain


class ChunkedBashTaskChain(NodeGeneratorChain, bapp.plugin_type()):
    """Simple bash batch commands with chunking support"""
    __slots__ = ()
    
    def __init__(self):
        """Setup chain"""
        super(ChunkedBashTaskChain, self).__init__()
        self.set_head(BashExecuteTaskGenerator())
        self.prepend_head(FrameSequenceGenerator())
        
    _plugin_name = "Bash Execution (Chunked)"

# end class ChunkedBashTaskChain




