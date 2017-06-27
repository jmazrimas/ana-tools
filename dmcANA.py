import os
import ctypes

# save local dir
local_directory = os.getcwd()
local_directory = local_directory + "\\"

# parse input params and put in object called 'inputs'
with open('in.txt') as f:
    lines = f.readlines()

    inputs = {}

    for line in lines:
        kv = line.rstrip().split("=")
        key = kv.pop(0).strip()
        value = "=".join(kv).strip()
        inputs[key] = value

# download the input file to the local dir
import filemanagement
filemanagement.download_data(inputs["inputFile"], "input.stp")

#os.chdir("C:\\scratch\\dmc\\ana\\Jun16-PDF-API-release")
print "Loading Create3DPdf DLL....\n"
convDll = ctypes.WinDLL("ModuleDLL/Create3DPdf.dll")

convDll.restype = ctypes.c_int
convDll.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

infile = "input.stp"
outfile = "test.stl"

print "Converting step file to stl...."
result = convDll.STPtoSTLConverter(infile, outfile)
print result
#print "... success!\n"

print "Loading MachiningAna DLL....\n"
machDll = ctypes.WinDLL("ModuleDLL/Machining/MachiningAna.dll")

machDll.restype = ctypes.c_char_p
machDll.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

infile = "test.stl"
outfile = "test.json"

print "Running analysis...."
result = machDll.MachiningAna_RunAnalysis(infile, outfile)
print result
#print "... success!\n"

convDll.restype = ctypes.c_int
convDll.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

infile = "test.json"
# outfile = "../../../test.pdf"
outfile = local_directory+"output.pdf"

print "Creating 3dPDF report...."
result = convDll.create3DPDF(infile, outfile)
print result
print "... success!\n"

final_name = filemanagement.upload_report(outfile)

outputs = "outputFile="+final_name
outputs += "\noutputTemplate=<div class=\"project-run-services padding-10\" ng-if=\"!runHistory\" layout=\"column\">          <style>            #custom-dome-UI {             margin-top: -30px;           }          </style>            <div id=\"custom-dome-UI\">             <div layout=\"row\" layout-wrap style=\"padding: 0px 30px\">               <h2>Report Created Successfully:</h2>               <p><a href=\"{{outputFile}}\">{{outputFile}}</a></p>             </div>           </div>        </div>   <script> </script>"

target = open("out.txt", 'w')
target.write(outputs)
target.close

