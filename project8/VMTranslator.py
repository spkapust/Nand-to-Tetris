
import sys
import re
from CodeWriter import CodeWriter
from Parser import Parser
import glob, os


path = sys.argv[1]
vmfiles = []
if os.path.isfile(path):
   vmfiles.append(path)
   withextension = os.path.basename(path)
   name = os.path.splitext(withextension)[0]
   path = os.path.dirname(path)
else:
    name = os.path.basename(path)
    for file in os.listdir(path):
        if file.endswith(".vm"):
            vmfiles.append(os.path.join(path, file))
for file in vmfiles:
    print(file)

print('now doing check commands \n')
print(path)
print(name)
c = CodeWriter(path,name)

print(len(vmfiles))
if len(vmfiles) > 1:
    c.startupcode()

for file in vmfiles:
    p=Parser(file)
    c.currentFile = os.path.splitext(os.path.basename(file))[0]
    c.segments['static'] = c.currentFile

    while(p.hasMoreCommands()):
        p.advance()
        #print(p.command, end="")
        print('//' + p.command)
        c.code.write('//' + p.command)
        tempcommand=p.command
        p.command = p.command.split()[0]
        commandtype = p.commandType()
        p.command = tempcommand
        #print(commandtype)
        if ( commandtype == 'C_ARITHMETIC'):
            c.writeArithmetic(p.command.split()[0])
        elif( commandtype == 'C_PUSH' or commandtype == 'C_POP'):
            com = p.command.split()
            pp =com[0] 
            segment = com[1]
            index = com[2] 
            c.WritePushPop(pp, segment, index)
        elif( commandtype == 'C_LABEL'):
            label = p.command.split()[1]
            c.writeLabel(label)
        elif( commandtype == 'C_GOTO'):
            label = p.command.split()[1]
            c.writeGoto(label)
        elif( commandtype == 'C_IF'):
            label = p.command.split()[1]
            c.writeIf(label)
        elif( commandtype == 'C_CALL'):
            functionName = p.command.split()[1]
            numArgs = p.command.split()[2]
            c.writeCall(functionName, numArgs)
        elif (commandtype == 'C_FUNCTION'):
            functionName = p.command.split()[1]
            numLocals = int(p.command.split()[2])
            c.writeFunction(functionName, numLocals)
        elif (commandtype == 'C_RETURN'):
            c.writeReturn()
   
    p.close()

c.close()
