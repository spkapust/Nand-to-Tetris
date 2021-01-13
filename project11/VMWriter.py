import os

class VMWriter:

    def __init__(self, file):
        folder = os.path.dirname(file.name)
        base = os.path.basename(file.name)
        name = os.path.splitext(base)[0] + ".vm"
        self.classname = os.path.splitext(base)[0]
        self.file = open(os.path.join(folder,name), "w+")
        

        return

    def writePush(self, segment, index):
        if segment == 'var': segment = 'local'
        if segment == 'arg': segment = 'argument'
        if segment == 'field': segment = 'this'
        if index == 'null': index = 0
        self.file.write("push " + segment  + " " + str(index) + "\n")
        
    def writePop(self, segment, index):
        if segment == "var": segment = 'local'
        if segment == 'arg': segment = 'argument'
        if segment == 'field': segment = 'this'
        self.file.write("pop " + segment  + " " + str(index) + "\n")
        
    def writeArithmetic(self, command):
        operators = {'+': 'add', 
                     '-': 'sub', 
                     '*': 'call Math.multiply 2', 
                     '/': 'call Math.divide 2', 
                     '&amp;':'and', 
                     '|':'or', 
                     '&lt;' : 'lt',
                     '&gt;' : 'gt',
                     '=': 'eq',
                     'neg' : 'neg',
                     '~': 'not'}
        command = operators[command]
        self.file.write(command + "\n")   

    def writeLabel(self, label):
        self.file.write("label " + label + "\n")   

    def writeGoto(self, label):
        self.file.write("goto " + label + "\n")

    def writeIf(self, label):
        self.file.write("if-goto " + label + "\n")

    def writeCall(self, name, nArgs):
        self.file.write("call " + name + " " + str(nArgs) + "\n" )

    def writeFunction(self, name, nLocals):
        self.file.write("function " + self.classname + "." + name  + " " + str(nLocals) + "\n" )

    def writeReturn(self):
        self.file.write("return\n")

    def close(self):
        self.file.close()




    

