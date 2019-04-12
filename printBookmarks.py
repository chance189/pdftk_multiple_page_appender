'''
###############################################################################
# Author: Chance Reimer
# Purpose: Print out bookmark information to see if it is useful
###############################################################################
'''

import os
import sys
import traceback
import time


#Must map the directory if it is not local to OS
directory = "C:\\SomeUser\SomeDir"  #Directory with the files of interest
saveDir = "C:\\SomeUser\SaveDir"  #IDontKnow
files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file)) and file[-4:] == ".pdf"]
print(files)
print("NUMBER OF FILES NEEDED TO DO THIS: {0}".format(len(files)))

os.chdir(directory)  #change our working directory

count = 0
for f in files:
    saveFile = os.path.join(saveDir, f[:-4]+".txt")
    print("Trying to save here: {0}, we are on line {1}".format(saveFile, count))
    cmdExecute = "pdftk \"{0}\" dump_data output \"{1}\"".format(f, saveFile)
    print("Executing CMD:\n{0}".format(cmdExecute))
    os.system(cmdExecute)
    count+=1
