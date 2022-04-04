from collections import OrderedDict
import BaseClasses

"""
Skeleton for user defined input format.
Can be used as a model to write a full format definition file or be completed to use for a simple format.
"""


class UserParticle(BaseClasses.BasicInfo):
    
    def __init__(self):
        self.fieldnames = [] #define the names of the fields of the inforamtion stored on one line 
        self.map = {}


class UserEventInfo(BaseClasses.BasicInfo):
    
    def __init__(self):
        self.fieldnames= [] #define the names of the fields of the inforamtion stored on one line                                                                                                                                                                              
        self.map = {}
    
class UserFile(BaseClasses.EvtFile):
    

    def read_events(self):
        """
        Reads the events store in the input file and stores the information in the relevant classes. 
        MUST BE REDEFINED for each file format.
        """
        nevts = 0
        infile = open(self.name, 'r')
        contents = list(filter(None,infile.read().splitlines()))
        
        #loops over the lines
        for line in contents:
            if line.split()[0] == 'start_of_event_tag': #starts an event when reading the right tag
                eventinfo = UserEventInfo()
                eventinfo.read(line)
                particles = []

            elif line.split()[0] =='end_of_event_tag': #ends the event when reading the right tag
                eventinfo.map['nparticles'] = len(particles)
                #self.events += [UserEvent(eventinfo,particles)]

            else:#if not start or end of event, read a particle line
                new_p = UserParticle()
                new_p.read(line)
                particles +=  [new_p]
