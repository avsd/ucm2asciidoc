"""
Python Library for XML serialization.
Copyright (c) David Avsajanishvili
"""

from xml.dom import pulldom
from base_xmls import *
import sys



class XmlSerializer:
    """
    XML Serialization/Deserialization
    """

    __all__ = ["deserialize", "deserializeString",
               "silent"]
    silent = False

    def __init__(self):
        self.parser = None
        self.bufsize = pulldom.default_bufsize

    def warn(self, message):
        if self.silent:
            return
        sys.stderr.write("WARNING: %s\n" % message)

    def do_deserialize(self,doc,rootType):
        """
        Performs actual deserialization from XML DOM instance
        """

        ret = rootType()
        elem_stack = []
        char_stack = ""

        def warn_assert_hasattr(objt, attrname):
            """
            Checks whether the Object has specified attribute
            and warns if not
            """
            if not hasattr(objt, attrname):
                #self.warn("%s class attribute is not defined for %s. Adding will be tried"
                #     % (attrname,objt))
                return True
            else:
                return False
        def setValue(objt, value):
            """
            Sets "Value" of the object, defined with _valuename variable.
            If objt is string, just strips and returns value. Otherwise,
            returns the object.
            """

            if isinstance(objt,XMLItem):
                if objt._valuename:
                    setattr(objt,objt._valuename,value.strip())
                return objt
            elif isinstance(objt,str) or isinstance(objt,unicode):
                return value.strip()
            else:
                raise "Invalid type of object for setting value - %s" % type(objt)
            

        for event,node in doc:

            if   event == pulldom.START_ELEMENT:

                par_itm = None               #Parent (current) item
                child_itm = None              #Child item

                #Determine type of element
                if not elem_stack:
                    child_itm = ret
                else:
                    par_itm = elem_stack[-1]    #Parent (current) item
                    
                    if isinstance(par_itm, list):
                        t = elem_stack[-2]._elements.get(node.nodeName, "")

                        if isinstance(t, type) and issubclass(t, XMLItem):
                            child_itm = t()
                        elif isinstance(t, str) or isinstance(t, unicode):
                            child_itm = ""
                        else:
                            raise Exception("Invalid element specification for List: %s" % t)
                        
                                 
                    elif isinstance(par_itm, str) or isinstance(par_itm, unicode):
                        self.warn("Unexpected element: %s. Will be skipped" % node.nodeName)
                    elif isinstance(par_itm,XMLItem) and node.nodeName in par_itm._elements:
                        
                        # Processing element depending on type:
                        t = par_itm._elements[node.nodeName]
                        
                        if  isinstance(t, type) and issubclass(t,XMLItem):      # Item Class
                            child_itm = t()
                        elif isinstance(t, str) or isinstance(t, unicode):  # Plain (string property)
                            child_itm = ""
                        elif isinstance(t, list):            # List of items
                            child_itm = []
                            pass
                        else:
                            raise Exception("Invalid element specification: %s" % t)
                    else:
                        self.warn('"%s" element is not defined, skipped' % node.nodeName)
                #endif (not elem_stack)


                # Parsing attributes
                if isinstance(child_itm, XMLItem):
                    for a,v in node.attributes.items():
                        if a in child_itm._attributes:
                            if child_itm._attributes[a]:
                                setattr(child_itm, child_itm._attributes[a], v)
                                    
                        else:
                            self.warn("Unknown attribute %s of element %s. Skipped" %
                                 (a,node.nodeName)
                                 )
                else:
                    if node.attributes.length:
                        self.warn("Unexpected attributes in %s node. Skipped" % node.nodeName)

                # Adding element to Stack
                elem_stack.append(child_itm)
                
            elif event == pulldom.END_ELEMENT:
                par_itm = None                  #Parent item
                child_itm = elem_stack.pop()    #Child (current) item

                if elem_stack:
                    par_itm = elem_stack[-1]

                if not elem_stack:
                    setValue(child_itm, char_stack)
                elif isinstance(par_itm, list):
                    child_itm = setValue(child_itm, char_stack)
                    par_itm.append(child_itm)
                elif isinstance(par_itm, str) or isinstance(par_itm, unicode):
                    #self.warn("Unexpected element: %s. Will be skipped" % node.nodeName)
                    pass
                elif isinstance(par_itm,XMLItem) and node.nodeName in par_itm._elements:
                    
                    # Processing element depending on type:
                    t = par_itm._elements[node.nodeName]
                    
                    if isinstance(t, type) and issubclass(t,XMLItem):   # Item Class
                        if isinstance(child_itm,XMLItem): 
                            # Setting item value
                            child_itm = setValue(child_itm, char_stack)
                            if warn_assert_hasattr(par_itm, child_itm._membername):
                                setattr(par_itm,
                                        child_itm._membername,
                                        [] if child_itm._ismultiple else None)
                            if child_itm._ismultiple:
                                getattr(par_itm, child_itm._membername).append(child_itm)
                            else:
                                setattr(par_itm, child_itm._membername, child_itm)
                                
                        else: #child_itm not XMLItem - ERROR
                            raise Exception("Internal error: child_itm must be XMLItem")
                            
                    elif isinstance(t, str) or isinstance(t, unicode):             # Plain (string property)
                        warn_assert_hasattr(par_itm, par_itm._elements[node.nodeName])
                        setattr(par_itm, par_itm._elements[node.nodeName], char_stack.strip())

                    elif isinstance(t, list):                             # List of items
                        par_itm._elements[node.nodeName] += child_itm

                    else:
                        raise Exception("Invalid element specification: %s" % t)
                else:
                    #self.warn("%s element is not defined, skipped" % node.nodeName)
                    pass
            
            elif event == pulldom.CHARACTERS:
                char_stack += node.data
        
            # Clearing character buffer
            if not event in (
                pulldom.CHARACTERS,
                pulldom.COMMENT,
                pulldom.IGNORABLE_WHITESPACE,
                pulldom.PROCESSING_INSTRUCTION):
                             char_stack = ""
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< END FOR
        return ret

    def deserialize(self, stream_or_filename, rootType):
        """
        Deserializes objects structure from XML stream or XML file.
        """

        doc = pulldom.parse(stream_or_filename, self.parser, self.bufsize)
        return self.do_deserialize(doc,rootType)

    def deserializeString(self, string, rootType):
        """
        Deserializes objects structure from string XML.
        """

        doc = pulldom.parseString(stream_or_filename, self.parser)
        return self.do_deserialize(doc,rootType)
