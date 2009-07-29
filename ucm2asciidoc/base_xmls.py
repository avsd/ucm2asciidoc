"""
Base Python XML schema
Copyright (c) David Avsajanishvili
"""


class XMLItem(object):
    """
    Base class for all XML items
    """

    _attributes = {}
    _elements = {}
    _membername = 'xmlitem'
    _ismultiple = False
    _valuename = None

    def __init__(self,ismultiple = None):
        if not (ismultiple is None):
            self._ismultiple = bool(ismultiple)
        self._membername = self.__class__.__name__.lower() + ('s' if self._ismultiple else '')

class XMLEnumItem(str):
    """
    Represents element, constrained as enumeration
    """
    #TODO!
    pass
