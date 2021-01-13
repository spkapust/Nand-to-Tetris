class Parser:
   
    def __init__(self, file):
       self.file=open(file, "r")
       self.lines = self.file.readlines()
       self.currentLine = 0
       self.command = ''
       self.commandTypes = {
           'add' : 'C_ARITHMETIC',
           'sub' : 'C_ARITHMETIC',
           'and' : 'C_ARITHMETIC',
           'not' : 'C_ARITHMETIC',
           'or'  : 'C_ARITHMETIC',
           'lt'  : 'C_ARITHMETIC',
           'gt'  : 'C_ARITHMETIC',
           'eq'  : 'C_ARITHMETIC',
           'neg' : 'C_ARITHMETIC',
           'push': 'C_PUSH',
           'pop' : 'C_POP',
           'function' : 'C_FUNCTION',
           'call' :'C_CALL',
           'return' : 'C_RETURN',
           'if-goto' : 'C_IF',
           'goto' :'C_GOTO',
           'label' : 'C_LABEL'
           }
   
    def close(self):
       self.file.close()

    def hasMoreCommands(self):
        if (self.currentLine == len(self.lines)):
            return False
        line = self.lines[self.currentLine]
        while ( (line[0] == '/') or (line[0] == '\n') ):
            self.currentLine += 1
            line = self.lines[self.currentLine]
        if (self.currentLine == len(self.lines)):
            return False
        else:
            return True
    
    def advance(self):
        line = self.lines[self.currentLine]
        self.currentLine += 1
        self.command = line
    
    def commandType(self):
        words = self.command.split()
        return self.commandTypes[words[0]]
        
    def arg1(self):
        words = self.command.split()
        return self.commandTypes[words[1]]

    def arg2(self):
        words = self.command.split()
        return int(self.commandTypes[words[2]])

    

