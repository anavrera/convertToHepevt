from __future__ import print_function #comment this line when using python3 
from collections import OrderedDict

class BasicInfo:

    """
    Base class for Particle and EventInfo
    """
    
    def __init__(self):
        self.fieldnames = [] #names of all the columns
        self.map = {} #dictionary linking the column name to the value


    def read(self,line):
        """
        Splits the content of a line and stores it in self.map
        """
        self.map =  dict(zip(self.fieldnames,map(float,line.split())))

    def print_info(self,title):
        """
        Prints the contents of self.map.
        """
        print('##############',title,'####################')
        for i in range(len(self.map)):
            print(list(self.map.keys())[i]," : ",list(self.map.values())[i])

class Event:
    """
    Base class for event information.
    Each event is defined by the event information and the particles information.
    """
    def __init__(self, eventinfo, particles):
        self.eventinfo = eventinfo
        self.particles = particles

class EvtFile:
    """
    Base class for file information.
    Stores all events in the file.
    The file reading function has to be defined for each input format. 
    """

    def __init__(self,filename):
        self.name = filename
        self.events = []

    def dump_file_info(self):
        for ev in self.events:
            ev.eventinfo.print_info("EVENT")
            print("Number of particles in event",len(ev.particles))
            for p in ev.particles:
                p.print_info("PARTICLE")
