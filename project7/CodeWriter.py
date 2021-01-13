import os

class CodeWriter:

    def __init__(self):
        self.segments = {
            'local':'LCL',
            'argument':'ARG',
            'this':'THIS',
            'that':'THAT',
            'static': '',
            'temp' : '5',
            'pointer':'3'
           }
        self.commands ={
            'add\n' : '2arg',
            'sub\n' : '2arg',
            'and\n' : '2arg',
            'or\n'  : '2arg',
            'not\n' : '1arg',
            'neg\n' : '1arg',
            'gt\n'  : 'branch',
            'lt\n'  : 'branch',
            'eq\n'  : 'branch'
            }

    def openNew(self, path):
        filename = os.path.splitext(path)[0] + '.asm'
        self.code = open(filename,'w+')
        withextension = os.path.basename(path)
        withoutextension = os.path.splitext(withextension)[0]
        self.segments['static']=withoutextension
        self.branchenum = 0;
        
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
            if (command == 'add\n'):
                self.code.write('M=M+D\n')      #M=M+D      M[998]=M[998]+
            elif (command == 'sub\n'):
                self.code.write('M=M-D\n')      #M=M-D
            elif (command =='or\n'):
                self.code.write('M=M|D')
            elif (command =='and\n'):
                self.code.write('M=M&D')
        elif(self.commands[command] == '1arg'):
            self.code.write('@SP\n')            #@SP        A = 0; M[0]=1000
            self.code.write('A=M-1\n')          #A=M-1      A = M[0] - 1 = 999
            if(command=='neg\n'):
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
            if(command == 'eq\n'):
                self.code.write('D;JEQ\n')          #A=M-1      A=M[0] - 1 = 998
            if(command == 'gt\n'):
                self.code.write('D;JGT\n')
            if(command == 'lt\n'):
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
      
        else:                                                   #POP
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
      
