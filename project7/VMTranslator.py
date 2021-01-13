import sys
import re
from CodeWriter import CodeWriter
from Parser import Parser
import glob, os

path = sys.argv[1]
vmfiles = []
if os.path.isfile(path):
    vmfiles.append(path)
    #withextension = os.path.basename(path)
    #withoutextension = os.path.splitext(withextension)[0]
    #print(withoutextension)
else:
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".vm"):
                vmfiles.append((os.path.join(root, file)))
for file in vmfiles:
    print(file)

c = CodeWriter()

for file in vmfiles:
    c.openNew(file)
    p=Parser(file)
#p = Parser(sys.argv[1])
#c = CodeWriter(name)



    while(p.hasMoreCommands()):
        p.advance()
        #print(p.command, end="")
        c.code.write('//' + p.command)
        commandtype = p.commandType()
        #print(commandtype)
        if ( commandtype == 'C_ARITHMETIC'):
            c.writeArithmetic(p.command)
        elif( commandtype == 'C_PUSH' or commandtype == 'C_POP'):
            com = p.command.split()
            pp =com[0] 
            segment = com[1]
            index = com[2] 
            c.WritePushPop(pp, segment, index)
        
    p.close()
    c.close()
    print('done')
