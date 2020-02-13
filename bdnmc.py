from __future__ import print_function # comment this line when using python3

class BdNMCEvent:

    def __init__(self, eventinfo, particles):
        self.eventinfo = eventinfo
        self.particles = particles

class BdNMCParticle:

    def __init__(self):
        self.map = {}
        self.fieldnames = ["px",
                           "py",
                           "pz",
                           "E",
                           "x",
                           "y",
                           "z",
                           "t"]


    def read(self,line):
        data = line.split()
        self.map =  dict(zip(self.fieldnames,map(float,data[1:])))
        self.map['name'] = data[0]

    def print_info(self):
        print('############## PARTICLE  ####################')
        for i in range(len(self.map)):
            print(list(self.map.keys())[i]," : ",list(self.map.values())[i])
        
class BdNMCEventInfo:

    def __init__(self):
        self.fieldnames = ["evt_id"]
        self.map={}

    def read(self,line):
        evt_id = list(filter(None,line.split()))[1]
        self.map["evt_id"] = int(evt_id) - 1

    def print_info(self):
        print('############## EVENT INFO ####################')
        for i in range(len(self.map)):
            print(list(self.map.keys())[i]," : ",list(self.map.values())[i])

class BdNMCFile:
    
    def __init__(self,filename, DM_mass, V_mass):
        self.name = filename
        self.events = []
        self.info = {}

        self.init_info(DM_mass, V_mass)


    def init_info(self, DM_mass=0, V_mass=0):
        self.info['eta'] = [221, 0.548, 0]
        self.info['pion'] = [111, 0.134, 0]
        self.info['V'] = [9999, V_mass, 2]
        self.info['rho'] = [113, 0.7755, 0]
        self.info['omega'] = [223, 0.7826, 0]
        self.info['proton'] = [2212, 0.9383, 0]
        self.info['neutron'] = [2112, 0.9396, 0]
        self.info['electron'] = [11, 0.000511, 0]
        self.info['Recoil_DM'] = [81, DM_mass, 1]
        self.info['DM'] = [81, DM_mass, 2]

        
    def dump_file_info(self):
        for ev in self.events:
            ev.eventinfo.print_info()
            for p in ev.particles:
                p.print_info()
        print("Number of events",len(self.events))

    def count_events(self):
        infile = open(self.name, 'r')
        last_line = infile.readlines()[-1]
        print(last_line.split()[1])
        infile.close()
        
    def read_events(self):
        nevts = 0
        infile = open(self.name, 'r')
        contents = list(filter(None,infile.read().splitlines()))
        for line in contents:

            #ignores first line
            if line.split()[0] == 'Run':
                continue
            
            elif line.split()[0] == 'event':
                eventinfo = BdNMCEventInfo()
                eventinfo.read(line)
                particles = []

            elif line.split()[0] =='endevent':
                eventinfo.map['nparticles'] = len(particles)
                self.events += [BdNMCEvent(eventinfo,particles)]

            else: 
                new_p = BdNMCParticle()
                new_p.read(line)
                new_p.map['pdg'] = self.info[new_p.map['name']][0]
                new_p.map['status'] = self.info[new_p.map['name']][2]
                new_p.map['m'] = self.info[new_p.map['name']][1]
                particles +=  [new_p]

