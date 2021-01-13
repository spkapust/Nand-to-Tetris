import sys, re, glob, os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

path = sys.argv[1]
jackFiles = []
if os.path.isfile(path):
   jackFiles.append(path)
else:
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".jack"):
             jackFiles.append(os.path.join(root, file))
    

for file in jackFiles:

    #Getting the name of the file correct
    folder = os.path.dirname(file)
    base = os.path.basename(file)
    name= os.path.splitext(base)[0] + "T.xml"
    fullPath = os.path.join(folder, name)
    
    #Open tokenizer file and temp file to hold tokens in better format for compilation engine
    t = JackTokenizer(file)
    ft = open(fullPath, "w+")
    temp = open(os.path.join(folder,"temp.txt"),'w+')
    
    ft.write("<tokens>\n")
    while (t.hasMoreTokens()):
       t.advance()
       ft.write("<" + t.type + "> " + t.token + " </" + t.type + ">\n" )
       temp.write(t.type + " " + t.token + "\n")
       
    ft.write("</tokens>")
    ft.close()
    t.file.close()
    
    #put temp file back at the start, open compilation file
    temp.seek(0)
    name= os.path.splitext(base)[0] + ".xml"
    fullPath = os.path.join(folder, name)
    fc = open(fullPath, "w+")
    c = CompilationEngine(temp, fc)
    if c.current == "keyword class\n":
        c.CompileClass()
        c.file.close()
    temp.close()
    #os.remove(os.path.join(folder,"temp.txt"))
    #print('file removed')


