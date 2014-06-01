#-*-coding:utf-8-*-
"""
@package btractor.interfaces
@brief Interfaces dealing with job submission using tractor data structures

@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
from __future__ import unicode_literals
__all__ = ['ITractorProcessDataProvider']

from butility import (abstractmethod,
                      Interface)


class ITractorProcessDataProvider(Interface):
    """An interface to allow access to tractor specific data for processes launched on the farm.
    
    Clients should use this interface to obtain additional information about their execution context, such 
    as configuration data they can use to alter their behaviour accordingly
    """
    __slots__ = ()

    # -------------------------
    ## @name Interface
    # @{
    
    @abstractmethod
    def data(self):
        """@return the data object tractor received for this process. It is any kind of python data structure.
        It will be a kvstore compatible struture that should only be accessed with the corresponding
        schemas.
        If there is no data, None will be returned.
        @see as_kvstore()"""
        
    @abstractmethod
    def as_kvstore(self):
        """@return a KeyValueStoreProvider initialized with the value of data(), or None if there is not data 
        available
        @note for convenience, this is implemneted here"""
    
    @abstractmethod    
    def set_progress(self, progress):
        """Communicate the given progress to tractor
        @param progress a value from 0 to 100, indicating the progress in percent. The value is unchecked, as
        tractor will just igore invalid progress values. """
        
    ## -- End Interface -- @}

# end class TractorInputData


class ITractorNodeGeneratorChainProvider(Interface):
    """An interface allowing to obtain a list of Plugin-Instances deriving from the NodeGeneratorChain type
    @note Override this implementation if you need anything more specific than all services that implement this
    base type"""
    __slots__ = ()
    
    # -------------------------
    ## @name Interface
    # @{
    
    @abstractmethod
    def chains(self):
        """@return a list of chains implementing the NodeGeneratorChain interface"""
    
    ## -- End Interface -- @}

    

# end class ITractorNodeGeneratorChainProvider
