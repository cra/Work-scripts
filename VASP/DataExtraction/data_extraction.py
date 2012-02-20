#!/usr/bin/env python
from os import listdir
from os.path import isdir
from linecache import getline
from numpy import array

class Outcar:

    def __init__(self, path):
        self.path = path
        self.total_cpu_time = 0
        self.extract_data()
    
    def extract_data(self):
        # Extracts the total CPU time in seconds
        f = open("%s/OUTCAR" % (self.path), 'r')
        for line in f:
            if 'Total CPU time' in line:
                self.total_cpu_time = line.split()[5]
        f.close()
            
class Oszicar:
    
    def __init__(self, path):
        self.path = path
        self.total_energy = 0
        self.all_energies = []
        self.extract_data()
    
    def extract_data(self):
        # Extracts the total energy from the last iteration        
        f = open("%s/OSZICAR" % (self.path), 'r')
        for line in f:
            if 'E0=' in line:
                self.all_energies.append(float(line.split()[4]))
        f.close()
        self.total_energy = self.all_energies[-1]

class Poscar:
    
    def __init__(self, path):
        self.path = path
        self.title = self.extract_title()
        self.formula_unit = self.extract_formula_unit()

    def extract_title(self):
        # Extracts the title line of the POSCAR        
        return getline("%s/POSCAR" % (self.path), 1)[:-1]

    def extract_formula_unit(self):
        # Extracts the formula unit from the POSCAR (by getting the most occurring atom type)
        counts = getline("%s/POSCAR" % (self.path), 7).split()
        maximum = counts[0]
        for count in counts:
            if count > maximum: maximum = count
        return maximum
            
class Kpoints:
    
    def __init__(self, path):
        self.path = path
        self.kpoints = self.extract_kpoints()
        self.mesh_type = self.extract_type()
        self.total_kpoints = self.kpoints[0] * self.kpoints[1] * self.kpoints[2]
        
    def __repr__(self):
        # Sets how the Kpoints class object is represented
        return "%ix%ix%i" % (self.kpoints[0], self.kpoints[1], self.kpoints[2])
    
    def extract_kpoints(self):
        # Extracts the k-points as an array
        line = getline("%s/KPOINTS" % self.path, 4).split()
        return array([int(line[0]), int(line[1]), int(line[2])])
    
    def extract_type(self):
        # Extracts the type of the k-mesh
        return getline("%s/KPOINTS" % self.path, 3).split()[0]

class Incar:
      
    def __init__(self, path):
        self.path = path
        self.encut = 0
        self.extract_data()
        
            
    def extract_data(self):
        f = open("%s/INCAR" % self.path, 'r')
        for line in f:
            if 'ENCUT' in line and '#ENCUT' not in line:
                self.encut = line.split('=')[1][:-1]
        f.close()

def find_data(path, list_of_paths):
    """Finds the paths to the result files"""
    directory_list = listdir(path)
    for item in directory_list:
        if item == 'OUTCAR':
            list_of_paths.append(path)
        elif isdir("%s/%s" % (path, item)):
            find_data("%s/%s" % (path, item), list_of_paths)


if __name__ == '__main__':
    print "data_extractor module"