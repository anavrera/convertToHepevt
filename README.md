# convertToHepevt: Conversion to hepevt format
Python script to convert different file formats to hepevt. 
Currently supports LHEF and BdNMC input files. 

## Usage

### Prerequisites
Having Python installed ! The code should work for both Python 2 and 3.

When using Python 3, comment the line 
```
from __future__ import print_function
```
in the BaseClasses.py file. 

### Run the code

The code is made to need the less amount of information possible about the content of the file. 
Run the code with 
```
python convertToHepevt.py format input_file output_file
```
For a BdNMC input, you will need to add the optional parameters --DM_mass and --V_mass. 

Run 
```
python convertToHepevt.py -h
```
for a complete list of available options. 

## Using your own input format
If your input format is not supported by the code, you can

### 1. Request it to be added
Just send a message with the input file attached. The new definition will added as soon as possible. 

### 3. Use the "user" input
The file *user.py* contains a skeleton format definition that can be easily completed to suit a simple input format.
Be careful to correctly implement the *read_events* function in the *UserFile* class. 
If too many modifications are necessary, see the following point.

### 3. Add it yourself
The *user.py* file definition can also be used as a template to write a new format definition. 
