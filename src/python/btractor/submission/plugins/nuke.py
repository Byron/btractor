#-*-coding:utf-8-*-
"""
@package btractor.submission.plugins.nuke
@brief Job Submission plugins

@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
from __future__ import unicode_literals
__all__ = ['NukeRenderTasksChain']


import bapp
from ...alf.generators import (NodeGeneratorChain,
                               FrameSequenceGenerator,
                               NukeRenderTaskGenerator )


class NukeRenderTasksChain(NodeGeneratorChain, bapp.plugin_type()):
    """Represents a generator chain which is preconfigured to support frame chunking as and simple rendering
    of all enabled write nodes in a script.
    
    @note for compatibility, its important not to include the Job generator in this chain
    """
    __slots__ = ()
    
    def __init__(self):
        """Setup the chain"""
        super(NukeRenderTasksChain, self).__init__()
        self.set_head(FrameSequenceGenerator(NukeRenderTaskGenerator()))
        
    _plugin_name = "Nuke Render"
        
# end class NukeRenderTasksChain


