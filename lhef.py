from __future__ import print_function # comment this line when using python3
import xml.etree.ElementTree as ET

class LHEEvent:

    def __init__(self, eventinfo, particles, weights=None, attributes=None):
        self.eventinfo = eventinfo
        self.particles = particles
        self.weights = weights
        self.attributes = attributes


class LHEParticle:
    
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
        self.map =  dict(zip(self.fieldnames,map(float,line.split())))
        if self.map['pdg'] == 5:
            self.map['pdg'] = 2112
        elif self.map['pdg'] == 6:
            self.map['pdg'] = 2212

    def print_info(self):
        print('############## PARTICLE  ####################')
        for i in range(len(self.map)):
            print(list(self.map.keys())[i]," : ",list(self.map.values())[i])

class LHEEventInfo:
    
    def __init__(self):
        self.fieldnames = ["nparticles", "pid", "weight", "scale", "aqed", "aqcd"]
        self.map={}

    def read(self,line):
        self.map =  dict(zip(self.fieldnames,map(float,line.split())))

    def print_info(self):
        print('############## EVENT INFO ####################')
        for i in range(len(self.map)):
            print(list(self.map.keys())[i]," : ",list(self.map.values())[i])


class LHEFile:

    def __init__(self,filename):
        self.name = filename
        self.events = []

        
    def dump_file_info(self):
        for ev in self.events:
            ev.eventinfo.print_info()
            print("Number of particles in event",len(ev.particles))
            for p in ev.particles:
                p.print_info()
                
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
                self.events += [LHEEvent(eventinfo,particle_objs)]

        print("Number of events: ", nevts)
