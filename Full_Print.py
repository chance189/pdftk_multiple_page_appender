'''
###############################################################################
# Author: Chance Reimer
###############################################################################
'''
import os
import sys
import traceback
import FindPagesToPrint

file_IDs = "Values_Of_Interest.txt"
lookUp = "Lookup.txt"

pdf_Path = "C:\\SomePath"
bookMarks_Path = "C:\\SomeUser\\SomePath"
save_Path = "C:\\SomeUser\\SomePath"

class Master_Print:

    def __init__(self):
        self.list_Containers = []
        self.list_Files_in_Directory = [file for file in os.listdir(pdf_Path) if os.path.isfile(os.path.join(pdf_Path, file)) and file[-4:] == ".pdf"]
        self.del_File_In_Directory(save_Path)
        self.IterNumber = 0

    def run(self):
        with open(file_IDs, "r") as file:
            for line in file:
                subject = line  #assign the value per line
                print("============================================")
                print("SUBJECT TYPE: {0}".format(subject[1:9]))  #change as necessary for lookup character
                self.lookUpContainers(subject[1:9]) #change as necessary for lookup character
                for master in self.list_Containers:
                    for item in self.list_Files_in_Directory:
                        if master in item:
                            print("MASTER MATCHED: {0} || FILE: {1}".format(master, item))
                            try:
                                find_Pages = FindPagesToPrint.PDF_Book_Mark_Parser(directory_Bookmarks=bookMarks_Path, fileName_PDF=item, searchValue=subject)
                                find_Pages.find_Page_Numbers()
                                #pdftk_Pages = find_Pages.gen_Print_List_Range()
                                pdftk_Pages = find_Pages.gen_Mod_Print()
                                self.Execute_Add_Pages(item, pdftk_Pages)
                            except Exception as e:
                                print("ERROR OCCURRED: {3}\nITEM: {0}\nMASTER: {1}\nFILE: {2}".format(subject, master, item, e))
                                #traceback.print_exc()  #the traceback is annoying
                            print("---------------------------------------")
                print("============================================")

        #Compile all files here
        self.build()
        self.Execute_Order_66()

    def Execute_Add_Pages(self, fileName, pagesToAdd):
        file_Source = "\""+os.path.join(pdf_Path, fileName)+"\""
        file_Dest = os.path.join(save_Path,"Jedi{0}".format(self.IterNumber))
        stringToExc = "pdftk A={0} cat {1}output {2}.pdf".format(file_Source, pagesToAdd, file_Dest)
        os.system(stringToExc)
        self.IterNumber += 1

    def del_File_In_Directory(self, directory):
        for delFile in os.listdir(directory):
            deletFile = os.path.join(directory, delFile)
            try:
                if os.path.isfile(deletFile):
                    os.remove(deletFile)
            except Exception:
                traceback.print_exc()

    def lookUpContainers(self, searchString):
        self.list_Containers.clear()
        with open(lookUp, "r") as file:
            for line in file:
                if searchString in line:
                    self.list_Containers.append(line[:9])
                    #print(line[:9])

    def build(self):
        os.chdir(save_Path)  #move to the desired path
        os.system("pdftk *.pdf cat output EndFile.pdf")  #outputs all pdf concatenated together

    def Execute_Order_66():
        print("Palpatine: \"DEW IT\"")
        for jedi in os.listdir(save_Path):
            if self.isJedi(jediName=jedi, jediPlanet=save_Path):
                os.remove(os.path.join(save_Path, jedi))
                print("The brave Jedi {0} has fallen.".format(jedi))

    def isJedi(self, jediName, jediPlanet):
        return os.path.isfile(os.path.join(jediPlanet, jediName)) and ("Jedi" in jediName)


if __name__ == "__main__":
    newM = Master_Print()
    newM.run()
