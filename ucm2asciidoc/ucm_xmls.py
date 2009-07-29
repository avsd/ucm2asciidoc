"""
Python XML schema for Use Case Maker
Copyright (c) David Avsajanishvili
"""

from base_xmls import *
from datetime import datetime

class UniqueItem(XMLItem):
    """
    Base class for all unique items
    """

    def __init__(self):

        self.UniqueID = ""
        self.Name = ""
        self.ID = 0
        self.Prefix = ""

        super(UniqueItem, self).__init__(True)
        
        self._attributes.update({
            'UniqueID'      :'UniqueID',
            'Name'          :'Name',
            'ID'            :'ID',
            'Prefix'        :'Prefix',
            })

class DescribedItem(UniqueItem):
    """
    Represents an Item with Description subitem only
    (Goals, OpenIssues, etc.)
    """
    def __init__(self):
        self.description = ""
        super(DescribedItem, self).__init__()
        self._elements.update({
            'Description':'description',
            })

class Attributes(XMLItem):
    """
    Item with set of attributes - Description, Notes and RelatedDocument
    """

    # Define RelatedDocument element class, used only here.
    class RelatedDocument(XMLItem):
        def __init__(self):
            self.filename = ""
            super(Attributes.RelatedDocument, self).__init__(True)
            self._elements.update({'FileName':'filename'})
        
    
    def __init__(self):
        self.description = ""
        self.notes = ""
        self.relateddocuments = []

        super(Attributes, self).__init__(False)

        self._elements.update({
            'Description'       :'description',
            'Notes'             :'notes',
            'RelatedDocuments'  :self.relateddocuments,
            'RelatedDocument'   :Attributes.RelatedDocument     
            })

        

class Actor(UniqueItem):
    """
    Represents an Actor instance
    """

    def __init__(self):
        self.goals = []
        
        super(Actor, self).__init__()

        self._elements.update({
            'Attributes':Attributes,
            'Goals':self.goals,
            'Goal':DescribedItem,
            })

class ActiveActor(XMLItem):
    """
    Reference to Actor (by UniqueID) with IsPrimary flag
    """

    def __init__(self):
        self.actorID = ""
        self.isPrimary = False

        super(ActiveActor, self).__init__(True)

        self._elements.update({
            'ActorUniqueID'     :'actorID',
            'IsPrimary'         :'isPrimary',
        })
    

    
    
#class Packages

class UseCaseStep(UniqueItem):
    """
    Step of Use Case
    """

    def __init__(self):
        self.description = ""
        self.childID = ""
        self.stepType = ""

        super(UseCaseStep, self).__init__()

        self._elements.update({
            'Description'   :'description',
            'ChildID'       :'childID',
            'Type'          :'stepType',
            })

    
class UseCase(UniqueItem):
    """
    Represents single Use Case
    """

    class Trigger(XMLItem):
        eventType = "External" #TODO: Enum
        description = ""
        def __init__(self):
            super(UseCase.Trigger, self).__init__(False)
            self._elements.update({'EventType':'eventType', 'Description':'description'})
            
    def __init__(self):
        self.steps = []
        self.openissues = []
        self.activeactors = []
        self.prose = ""
        self.preconditions = ""
        self.postconditions = ""
        self.release = ""
        self.assignedTo = ""
        self.priority = 0
        self.complexity = "Low" #TODO: Enum
        self.implementation = "Scheduled" #TODO: Enum
        self.level = "Summary" #TODO: Enum
        self.status = "Named" #TODO: Enum
        self.trigger = None

        super(UseCase, self).__init__()

        self._elements.update({
            'Attributes'    :Attributes,
            'Steps'         :self.steps,
            'Step'          :UseCaseStep,
            'OpenIssues'    :self.openissues,
            'OpenIssue'     :DescribedItem,
            'ActiveActors'  :self.activeactors,
            'ActiveActor'   :ActiveActor,
            #'HistoryItems'  :asdf,
            'Prose'         :'prose',
            'Preconditions' :'preconditions',
            'Postconditions':'postconditions',
            'Release'       :'release',
            'AssignedTo'    :'assignedTo',
            'Priority'      :'priority',
            'Complexity'    :'complexity',
            'Implementation':'implementation',
            'Level'         :'level',
            'Status'        :'status',
            'Trigger'       :UseCase.Trigger
            
            })
    
        
#class Requirements
#class Glossary
#class Stakeholders



class Model(UniqueItem):
    """
    Model element
    """

    def __init__(self):
        self.author = ""
        self.company = ""
        self.release = ""
        self.creationdate = datetime.min
        
        self.actors = []
        self.usecases = []

        super(Model, self).__init__()
        self._ismultiple = False
        self._membername = "model"
       
        self._attributes.update({
            'Author'        :'author',
            'Company'       :'company',
            'Release'       :'release',
            'CreationDateValue'  :'creationdate'
            })

        self._elements.update({
            'Actors':       self.actors,
            'Actor':        Actor,
            #'Packages':     Packages,
            'UseCases':     self.usecases,
            'UseCase':      UseCase,
            #'Requirements': Requirements,
            'Attributes':   Attributes,
            #'Glossary':     Glossary,
            #'Stakeholders': Stakeholders
            })

class UCMDocument(XMLItem):
    """
    Root node class for UML Document
    """

    def __init__(self):
        self.Version = 0.0
        self.model = None

        super(UCMDocument, self).__init__()
       
        self._attributes.update({
            'xmlns:xsi':None,
            'xmlns:xsd':None,
            'Version':'Version'
            })

        self._elements.update({
            'Model':       Model
            })
