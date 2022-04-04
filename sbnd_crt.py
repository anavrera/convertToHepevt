from collections import OrderedDict
import numpy as np
import BaseClasses


class SbndCRTParticle(BaseClasses.BasicInfo):
    """
    Stores information about the particle (position, momentum,etc...)
    """
    def __init__(self):
        """
        Override the init function to define the correct field names
        """
        self.fieldnames = [
            "E", #positron energy
            "px", #positron momentum
            "py",
            "pz",
        ]


    def read(self,line,name,vtx,w):
        """
        Splits the content of a line and stores it in self.map
        """

        self.map =  dict(zip(self.fieldnames,map(float,line)))

        self.map['name']   = name
        self.map['vtx_z']  = vtx
        self.map['weight'] = w    
    


    

class SbndCRTEventInfo(BaseClasses.BasicInfo):
     
    """
    Stores information about the event (number of particles, events number, etc...)
    If not stored in the file, values have to be computed  manually when reading the file.
    Event number and number of particles are required 
    """
     
    def __init__(self,evt,nparticles):
         self.fieldnames = ["evt_id","nparticles"]
         self.map={}
         self.map['evt_id'] = evt
         self.map['nparticles'] = nparticles



class SbndCRTFile(BaseClasses.EvtFile):

    def __init__(self,filename, DN_mass):
        self.name = filename
        self.events = []
        self.info = {}

        self.init_info(DN_mass)

    def init_info(self, DN_mass=0):
        """
        General information about particles available in the file
        Format is: [pdg_code, mass, status (1 for tracked particles)]
        """

        self.info['electron'] = [11, 0.000511, 1]
        self.info['positron'] = [-11, 0.000511, 1]
        self.info['dark_neutrino'] = [81, DN_mass, 0]
    

    def read_events(self):
        """
        This function MUST be defined in your format definition file.
        It will read all the events of the file and fill the particles and event info.
        Specific to each format.
        """
        nevts = 0
        particles = []

        infile = open(self.name, 'r')
        contents = list(filter(None,infile.read().splitlines()[1:])) #skip the first line
        
        #loops over the lines
        for line in contents:

            eventinfo = SbndCRTEventInfo(nevts,2)
            particles = []
        
            splitline = line.split()
         
            electron = SbndCRTParticle()
            electron.read(splitline[:4],"electron",splitline[9],splitline[10])
            electron.map['pdg'] = self.info[electron.map['name']][0]
            electron.map['status'] = self.info[electron.map['name']][2]
            electron.map['m'] = self.info[electron.map['name']][1]
            
            #electron.print_info("electron")

            positron = SbndCRTParticle()
            positron.read(splitline[4:8],"positron",splitline[9],splitline[10])
            positron.map['pdg'] = self.info[positron.map['name']][0]
            positron.map['status'] = self.info[positron.map['name']][2]
            positron.map['m'] = self.info[positron.map['name']][1]
            #positron.print_info("positron")

            
            dark_neutrino = SbndCRTParticle()
            dark_neutrino.read([splitline[8],"0","0","0"],"dark_neutrino",splitline[9],splitline[10])
            dark_neutrino.map['pdg'] = self.info[dark_neutrino.map['name']][0]
            dark_neutrino.map['status'] = self.info[dark_neutrino.map['name']][2]
            dark_neutrino.map['m'] = self.info[dark_neutrino.map['name']][1]

            particles +=  [electron]
            particles +=  [positron]
            particles +=  [dark_neutrino]
                
            self.events += [BaseClasses.Event(eventinfo,particles)]
            nevts+=1