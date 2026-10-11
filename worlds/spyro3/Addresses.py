import abc
from abc import abstractmethod


class RAM(abc):
    address11Mapping = {}
    @abstractmethod
    def getAddress(self, addressName):
        pass

class NTSCU11RAM(RAM):
    def getAddress(self, addressName):
        return self.address11Mapping[addressName]

class NTSCU10RAM(RAM):
    address10Mapping = {}
    def getAddress(self, addressName):
        if addressName in self.address10Mapping:
            return self.addressMapping[addressName]
        else:
            return self.address11Mapping[addressName] - 0xE0
