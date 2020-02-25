import xml.etree.ElementTree as ET
from collections import OrderedDict
import BaseClasses

class LHEParticle(BaseClasses.BasicInfo):
    
    def __init__(self):
        self.fieldnames = ["pdg",
                           "status",
                           "mother1",
                           "mother2",
                           "color1",
                           "color2",
                           "px",
                           "py",
                           "pz",
                           "E",
                           "m",
                           "lifetime",
                           "spin"]
        self.map={}

    def read(self,line):
        self.map =  OrderedDict(zip(self.fieldnames,map(float,line.split())))
        if self.map['pdg'] == 5:
            self.map['pdg'] = 2112
        elif self.map['pdg'] == 6:
            self.map['pdg'] = 2212

class LHEEventInfo(BaseClasses.BasicInfo):
    
    def __init__(self):
        self.fieldnames = ["nparticles", "pid", "weight", "scale", "aqed", "aqcd"]
        self.map={}


class LHEFile(BaseClasses.EvtFile):
                
    def read_events(self):
        tree = ET.parse(self.name)
        root = tree.getroot()
        nevts=0
        for element in root:
            if element.tag == "event":
                eventinfo = LHEEventInfo()
                data = list(filter(None,element.text.splitlines()))
                eventdata, particles = data[0], data[1:]
                eventinfo.read(eventdata)
                eventinfo.map['evt_id'] = nevts

                particle_objs = []
                for p in particles:
                    particle = LHEParticle()
                    particle.read(p)
                    particle_objs += [particle]
                nevts+=1
                self.events += [BaseClasses.Event(eventinfo,particle_objs)]

