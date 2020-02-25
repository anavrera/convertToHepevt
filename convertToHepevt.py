import os,sys
import argparse
import xml.etree.ElementTree as ET
import random


import lhef
import bdnmc
#import user



def generate_position(particle, dist_file=None):
    
    """
    Generates random starting position for the particle. 
    This should be adjusted tu suit the user's needs.
    Default is for SBND.
    """
    
    x = random.uniform(0,1)*400-200;
    y = random.uniform(0,1)*400-200;
    z = random.uniform(0,1)*500;
    
    particle.map['x'] = x
    particle.map['y'] = y
    particle.map['z'] = z
    
def generate_mother(particle,mom1=0,mom2=0):
    """
    Generates parent particle information.
    Default values are 0. 
    """

    particle.map['mother1'] = mom1
    particle.map['mother2'] = mom2

def generate_children(particle,child1=0,child2=0):
    
    """
    Generate daughter particle information. 
    Default values are 0
    """

    particle.map['child1'] = child1
    particle.map['child2'] = child2

def generate_time(particle):

    """
    Generate time information for a particle.
    Default value is 0. 
    """
    particle.map['t'] = 0

def dump_file_info(events):
    """
    Prints all the events in the file.
    """
    for ev in events:
        ev.eventinfo.print_info()
        for p in ev.particles:
            p.print_info()

def check_info(events):
    """
    Checks information stored in input events
    Missing information is generated randomly if needed    
    """
    for ev in events:
        for p in ev.particles:
            keys = p.map.keys()
            if 'x' not in keys:
                generate_position(p)

            if 'mother1' not in keys:
                generate_mother(p)

            if 'child1' not in keys:
                generate_children(p)

            if 't' not in keys:
                p.map['t'] = 0

        
            
def write_hepevt(events, outfile_name):
    
    """
    Writes the events in hepevt format
    """
    
    names_ev = ['evt_id','nparticles']
    names_p  = ['status', 'pdg', 'mother1', 'mother2', 'child1', 'child2','px', 'py', 'pz', 'E', 'm', 'x', 'y', 'z', 't']
    
    outfile = open(outfile_name,'w')

    for ev in events:
        str_evt_info = ""
        for name in names_ev:
            str_evt_info += str(int(ev.eventinfo.map[name]))
            str_evt_info += " " 
        outfile.write(str_evt_info + '\n')
        
        for p in ev.particles:
            str_particle = ""
            count=0
            for name in names_p:
                if count <=5:
                    str_particle += str(int(p.map[name]))
                else:
                    str_particle += str(p.map[name])
                str_particle += " "
                count+=1
            outfile.write(str_particle + '\n')

    outfile.close()


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Converts files to hepevt format")
    
    # Positional arguments
    parser.add_argument("format", help="Input file format. Formats currently supported: lhef, bdnmc or user defined")
    parser.add_argument("input_filename", help="Input file name")
    parser.add_argument("output_filename", help="Output file name")

    # Optional arguments 
    parser.add_argument("--DM_mass", help="Mass of the DM particle (GeV/c) (required for BdNMC input files)")
    parser.add_argument("--V_mass", help="Mass of the dark photon (GeV/c) (required for BdNMC input files)")

    args = parser.parse_args()

    if args.format=="lhef":
        infile = lhef.LHEFile(args.input_filename)
    
    elif args.format=="bdnmc":
        if args.DM_mass == None or args.V_mass == None:
            sys.exit("\n\nERROR: DM mass and V mass required for BdNMC input\n Run python convertToHepevt -h for a list of available options\n")
        else:
            infile = bdnmc.BdNMCFile(args.input_filename, args.DM_mass, args.V_mass)

    elif args.format=="user":
        infile = user.UserFile(args.input_filename)

    else:
        sys.exit("\n\nERROR: File format not supported !\n Inputs accepted: bdnmc, lhef or user\n Run python convertToHepevt -h for a list of available options.")
        
    infile.read_events()
    infile.dump_file_info()
    check_info(infile.events)
    write_hepevt(infile.events, args.output_filename)
