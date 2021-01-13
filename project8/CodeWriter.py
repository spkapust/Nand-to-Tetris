import os

class CodeWriter:

    def __init__(self, path, name):
        self.segments = {
            'local':'LCL',
            'argument':'ARG',
            'this':'THIS',
            'that':'THAT',
            'static': '',
            'temp' : '5',
            'pointer':'3',
            'static' : ''
           }
        self.commands ={
            'add' : '2arg',
            'sub' : '2arg',
            'and' : '2arg',
            'or'  : '2arg',
            'not' : '1arg',
            'neg' : '1arg',
            'gt'  : 'branch',
            'lt'  : 'branch',
            'eq'  : 'branch'
            }
        
        filename = os.path.join(path, name + '.asm')
        self.code = open(filename,'w+')
        self.branchenum = 0
        self.returnenum = 0
        self.currentFile = ''
        
    def close(self):
        self.code.close()

    def writeArithmetic(self, command):
        
        if(self.commands[command] == '2arg'):
            #add or sub
            self.code.write('@SP\n')            #@SP        A = 0; M[0]=1000
            self.code.write('A=M-1\n')          #A=M-1      A = M[0] - 1 = 999
            self.code.write('D=M\n')            #D=M        D = M[999]
            self.code.write('@SP\n')            #@SP        A = 0 
            self.code.write('M=M-1\n')          #M=M-1      M[0] = M[0] - 1 = 999
            self.code.write('A=M-1\n')          #A=M-1      A=M[0] - 1 = 998
            #print(command)
            if (command == 'add'):
                self.code.write('M=M+D\n')      #M=M+D      M[998]=M[998]+
            elif (command == 'sub'):
                self.code.write('M=M-D\n')      #M=M-D
            elif (command =='or\n'):
                self.code.write('M=M|D')
            elif (command =='and'):
                self.code.write('M=M&D')
        elif(self.commands[command] == '1arg'):
            self.code.write('@SP\n')            #@SP        A = 0; M[0]=1000
            self.code.write('A=M-1\n')          #A=M-1      A = M[0] - 1 = 999
            if(command=='neg'):
                self.code.write('M=-M\n')            
            else: 
                self.code.write('M=!M\n') 
        elif(self.commands[command] == 'branch'):
            self.code.write('@SP\n')            #@SP        A = 0; M[0]=1000
            self.code.write('A=M-1\n')          #A=M-1      A = M[0] - 1 = 999
            self.code.write('D=M\n')            #D=M        D = M[999]
            self.code.write('@SP\n')            #@SP        A = 0 
            self.code.write('M=M-1\n')          #M=M-1      M[0] = M[0] - 1 = 999
            self.code.write('A=M-1\n')          #A=M-1      A=M[0] - 1 = 998
            self.code.write('D=M-D\n')          #A=M-1      A=M[0] - 1 = 998
            self.code.write('M=-1\n')            #A=M-1      A=M[0] - 1 = 998
            self.code.write('@IF_' + str(self.branchenum) + '\n')
            if(command == 'eq'):
                self.code.write('D;JEQ\n')          #A=M-1      A=M[0] - 1 = 998
            if(command == 'gt'):
                self.code.write('D;JGT\n')
            if(command == 'lt'):
                self.code.write('D;JLT\n')
            self.code.write('@SP\n')
            self.code.write('A=M-1\n')
            self.code.write('M=!M\n')
            self.code.write('(IF_' + str(self.branchenum) +')\n')
            self.branchenum = self.branchenum + 1
    
    def WritePushPop(self, command, segment, index):
        if(segment != 'constant'):
            symbol = self.segments[segment]
            if (segment == 'static'): symbol = symbol + '.' + index
        if(command=='push'):                                    #PUSH  
            if (segment == 'static'):
                self.code.write('@' + symbol + '\n')
                self.code.write('D=M\n')
            else:    
                self.code.write('@'+index+'\n')                     #@index
                self.code.write('D=A\n')                            #D=A   
                if(segment != 'constant'):
                        self.code.write('@' + symbol + '\n')        #@segment
                        if( (segment != 'temp') & (segment != 'pointer') & (segment != 'static')):
                               self.code.write('A=M\n')                    #A=M
                        self.code.write('A=D+A\n')                  #A=D+A      
                        self.code.write('D=M\n')                    #D=M         
            self.code.write('@SP\n')                            #@SP
            self.code.write('A=M\n')                            #A=M
            self.code.write('M=D\n')                            #M=D
            self.code.write('@SP\n')                            #@SP
            self.code.write('M=M+1\n')                          #M=M+1
      
        else:    
            if (segment == 'static'):
                self.code.write('@SP\n')
                self.code.write('M=M-1\n')
                self.code.write('A=M\n')
                self.code.write('D=M\n')
                self.code.write('@' + symbol + '\n')
                self.code.write('M=D\n')
            else:
                self.code.write('@'+symbol+'\n')                    #@segment
                if (segment == 'temp' or segment == 'pointer' or segment == 'static'):
                    self.code.write('D=A\n')
                else: self.code.write('D=M\n')                            #D=M
                self.code.write('@'+index+'\n')                     #@index
                self.code.write('D=D+A\n')                          #D=D+A
                self.code.write('@SP\n')                            #@SP
                self.code.write('M=M-1\n')                          #M=M-1
                self.code.write('A=M\n')                            #A=M
                self.code.write('D=D+M\n')                          #D=D+M      D= Address + Value
                self.code.write('A=M\n')                            #A=M        A = Value
                self.code.write('A=D-A\n')                          #A=D-A      A = Address
                self.code.write('D=D-A\n')                          #D=D-A      D = Value
                self.code.write('M=D\n')            
  
    def writeLabel(self, label):
        self.code.write('(' + self.currentFile + '$' + label +')\n')
    
    def writeGoto(self, label):
        self.code.write('@'+ self.currentFile + '$' + label  +'\n')
        self.code.write('0;JMP\n')
    
    def writeIf(self, label):
        self.code.write('@SP\n')
        self.code.write('M=M-1\n')
        self.code.write('A=M\n')
        self.code.write('D=M\n')
        self.code.write('@'+ self.currentFile + '$' + label  +'\n')
        self.code.write('D;JNE\n')

    def writeCall(self, functionName, numArgs):
        self.code.write('@return-address-' + str(self.returnenum) +'\n')
        self.code.write('D=A\n')
        self.code.write('@SP\n')
        self.code.write('A=M\n')
        self.code.write('M=D\n')
        self.code.write('@SP\n')
        self.code.write('M=M+1\n')

        self.code.write('@LCL\n')
        self.code.write('D=M\n')
        self.code.write('@SP\n')
        self.code.write('A=M\n')
        self.code.write('M=D\n')
        self.code.write('@SP\n')
        self.code.write('M=M+1\n')

        self.code.write('@ARG\n')
        self.code.write('D=M\n')
        self.code.write('@SP\n')
        self.code.write('A=M\n')
        self.code.write('M=D\n')
        self.code.write('@SP\n')
        self.code.write('M=M+1\n')

        self.code.write('@THIS\n')
        self.code.write('D=M\n')
        self.code.write('@SP\n')
        self.code.write('A=M\n')
        self.code.write('M=D\n')
        self.code.write('@SP\n')
        self.code.write('M=M+1\n')

        self.code.write('@THAT\n')
        self.code.write('D=M\n')
        self.code.write('@SP\n')
        self.code.write('A=M\n')
        self.code.write('M=D\n')
        self.code.write('@SP\n')
        self.code.write('M=M+1\n')

        self.code.write('@' + numArgs + '\n')
        self.code.write('D=A\n')
        self.code.write('@5\n')
        self.code.write('D=D+A\n')
        self.code.write('@SP\n')
        self.code.write('D=M-D\n')
        self.code.write('@ARG\n')
        self.code.write('M=D\n')

        self.code.write('@SP\n')
        self.code.write('D=M\n')
        self.code.write('@LCL\n')
        self.code.write('M=D\n')

        self.code.write('@' + functionName + '\n')
        self.code.write('0;JMP\n')

        self.code.write('(return-address-' + str(self.returnenum) +')\n')
        self.returnenum += 1

    def writeFunction(self, functionName, numLocals):
        self.code.write('(' + functionName + ')\n')

        for x in range (0, numLocals):
            self.code.write('@SP\n')
            self.code.write('A=M\n')
            self.code.write('M=0\n')
            self.code.write('@SP\n')
            self.code.write('M=M+1\n')

    def writeReturn(self):
        #FRAME = LCL
        self.code.write('@LCL\n')
        self.code.write('D=M\n')
        self.code.write('@R13\n')
        self.code.write('M=D\n')

        #RET = *(FRAME-5)
        self.code.write('@5\n')
        self.code.write('A=D-A\n')
        self.code.write('D=M\n')
        self.code.write('@R14\n')
        self.code.write('M=D\n')

        #*ARG = pop()
        self.code.write('@SP\n')
        self.code.write('M=M-1\n')
        self.code.write('A=M\n')
        self.code.write('D=M\n')
        self.code.write('@ARG\n')
        self.code.write('A=M\n')
        self.code.write('M=D\n')
        
        #SP=ARG+1
        self.code.write('@ARG\n')
        self.code.write('D=M+1\n')
        self.code.write('@SP\n')
        self.code.write('M=D\n')

        #THAT = *(FRAME-1)
        self.code.write('@R13\n')
        self.code.write('A=M-1\n')
        self.code.write('D=M\n')
        self.code.write('@THAT\n')
        self.code.write('M=D\n')

        #THIS = *(FRAME-2)
        self.code.write('@R13\n')
        self.code.write('A=M-1\n')
        self.code.write('A=A-1\n')
        self.code.write('D=M\n')
        self.code.write('@THIS\n')
        self.code.write('M=D\n')

        #ARG = *(FRAME-3)
        self.code.write('@R13\n')
        self.code.write('A=M-1\n')
        self.code.write('A=A-1\n')
        self.code.write('A=A-1\n')
        self.code.write('D=M\n')
        self.code.write('@ARG\n')
        self.code.write('M=D\n')

        #LCL = *(FRAME-4)
        self.code.write('@4\n')
        self.code.write('D=A\n')
        self.code.write('@R13\n')
        self.code.write('A=M-D\n')
        self.code.write('D=M\n')
        self.code.write('@LCL\n')
        self.code.write('M=D\n')

        #goto RET
        self.code.write('@R14\n')
        self.code.write('A=M\n')
        self.code.write('0;JMP\n')

    def startupcode(self):
        self.code.write('@256\n')
        self.code.write('D=A\n')
        self.code.write('@SP\n')
        self.code.write('M=D\n')
        self.writeCall('Sys.init', '0')

