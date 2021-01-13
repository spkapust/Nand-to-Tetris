import os
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine:

    def __init__(self, tokens, file):
        self.tokens = tokens
        self.file = file
        self.line = 1
        self.current = self.tokens.readline()
        self.st = SymbolTable()
        self.vm = VMWriter(file)
        self.whiles = 0
        self.ifs = 0
        base = os.path.basename(file.name)
        self.ccname = os.path.splitext(base)[0]
        return

    def CompileClass(self):
        self.file.write("<class>\n")
        self.writeAtom() #class
        self.writeAtom() #className
        self.writeAtom() #{
        while (self.current.split()[1] != "}"):
            keyword = self.current.split()[1]
            if ( (keyword == "static") | (keyword =="field") ):
                self.compileClassVarDec()
            elif ( (keyword == "constructor") | (keyword =="function") | (keyword =="method") ):
                self.compileSubroutine()
        self.writeAtom() #}
        self.file.write("</class>")
        self.vm.close()
        return

    def compileClassVarDec(self):
        self.file.write("<classVarDec>\n")
        
        kind = self.current.split()[1]
        self.writeAtom() #static or field
        
        type = self.current.split()[1]
        self.writeAtom() #type
        
        name = self.current.split()[1]
        self.writeAtom() # varName

        self.st.define(name, type, kind)
        self.file.write(self.st.kindOf(name) + " " + self.st.typeOf(name) + " " + str(self.st.indexOf(name)) + "\n")
          
        while(self.current.split()[1] != ';'):
            self.writeAtom() #,
            name = self.current.split()[1]
            self.writeAtom() #varName
            
            self.st.define(name, type, kind)
            self.file.write(self.st.kindOf(name) + " " + self.st.typeOf(name) + " " + str(self.st.indexOf(name)) + "\n")   
        
        self.writeAtom() #;  
        self.file.write("</classVarDec>\n")
        return

    def compileSubroutine(self):
        self.file.write("<subroutineDec>\n")
        self.st.startSubroutine()

        ismethod = (self.current.split()[1] == "method")
        isconstructor = (self.current.split()[1] == "constructor")
        #if (ismethod | isconstructor): self.st.define('this', self.ccname, 'arg') 
        self.writeAtom() #constructor, function, or method

        void = self.current.split()[1] == 'void'
        self.writeAtom() #void or type

        name = self.current.split()[1]
        self.writeAtom() #subRoutine Name

        if ismethod: self.st.define('this', self.ccname, 'arg')
        self.writeAtom() #(
        self.compileParameterList()
        self.writeAtom() #)
        

        self.file.write("<subroutineBody>\n")
        self.writeAtom() #{
        while(self.current.split()[1] == 'var'):
            self.compileVarDec()
        
        nLocals = 0
        for key in self.st.subTable:
            if (self.st.subTable[key]['kind'] == 'var'):
                nLocals += 1
        self.vm.writeFunction(name, nLocals)
        if isconstructor:
            nfields = 0
            for key in self.st.classTable:
                if (self.st.classTable[key]['kind'] == 'field'):
                    nfields += 1
            self.vm.writePush('constant', nfields)
            self.vm.writeCall('Memory.alloc', 1)
            self.vm.writePop('pointer',0)
        if ismethod:
            self.vm.writePush('arg', 0)
            self.vm.writePop('pointer', 0)
            
            

        while(self.current.split()[1] in ['let', 'if', 'while', 'do', 'return']):
            self.compileStatements()
        self.writeAtom() #}
        self.file.write("</subroutineBody>\n")

        self.file.write("</subroutineDec>\n")
        return

    def compileParameterList(self):
        self.file.write("<parameterList>\n")
        if self.current.split()[0] != 'symbol':
            
            kind = "arg"
            
            type = self.current.split()[1] 
            self.writeAtom() #type
           
            name = self.current.split()[1]
            self.writeAtom() #varName

            self.st.define(name,type,kind)
            self.file.write(self.st.kindOf(name) + " " + self.st.typeOf(name) + " " + str(self.st.indexOf(name)) + "\n")
            

            while(self.current.split()[1] == ','):
                self.writeAtom() #,

                type = self.current.split()[1]
                self.writeAtom() #type

                name = self.current.split()[1]
                self.writeAtom() #varName

                self.st.define(name,type,kind)
                self.file.write(self.st.kindOf(name) + " " + self.st.typeOf(name) + " " + str(self.st.indexOf(name)) + "\n")
        
        self.file.write("</parameterList>\n")
        return

    def compileVarDec(self):
        self.file.write("<varDec>\n")

        kind = self.current.split()[1]
        self.writeAtom() #var
        
        type = self.current.split()[1]
        self.writeAtom() #type

        name = self.current.split()[1]
        self.writeAtom() #varname

        self.st.define(name,type,kind)
        self.file.write(self.st.kindOf(name) + " " + self.st.typeOf(name) + " " + str(self.st.indexOf(name)) + "\n")

        while(self.current.split()[1] != ';'):
            self.writeAtom() #,

            name = self.current.split()[1]
            self.writeAtom() #varName

            self.st.define(name,type,kind)
            self.file.write(self.st.kindOf(name) + " " + self.st.typeOf(name) + " " + str(self.st.indexOf(name)) + "\n")

        self.writeAtom() #;
        self.file.write("</varDec>\n")
        return

    def compileStatements(self):
        self.file.write("<statements>\n")
        while(self.current.split()[1] in ['let','if','while','do','return']):
            st = self.current.split()[1]
            if st == 'let': self.compileLet()
            elif st == 'if': self.compileIf()
            elif st == 'while': self.compileWhile()
            elif st == 'do': self.compileDo()
            elif st == 'return': self.compileReturn()
        self.file.write("</statements>\n")
        return

    def compileDo(self):
        self.file.write("<doStatement>\n")
        self.writeAtom()#do
        
        self.compileSubroutineCall()
        #pos = self.tokens.tell()
        #nextsym =self.tokens.readline().split()[1]
        #self.tokens.seek(pos)
        
        
        #if nextsym == '.':
        #    self.writeAtom()#className or varName
        #    self.writeAtom() #.
        #self.writeAtom() #subroutine name
        #self.writeAtom() #(
        #self.compileExpressionList()
        #self.writeAtom() #)
        
        self.writeAtom() # ;
        self.file.write("</doStatement>\n")
        self.vm.writePop("temp", 0)
        return

    def compileLet(self):
        self.file.write("<letStatement>\n")
        arr = False
        self.writeAtom() #let
        name = self.current.split()[1]
        segment = self.st.kindOf(name)
        index = self.st.indexOf(name)
        self.writeAtom() #varName
        if(self.current.split()[1] == '['):
            arr = True
            
            self.writeAtom() #[
            self.compileExpression() #expression
            self.writeAtom() #]

            self.vm.writePush(segment, index)
            self.vm.writeArithmetic('+')
        self.writeAtom() #=
        self.compileExpression() #expression
        self.writeAtom() #;

        #segment = self.st.kindOf(name)
        #index = self.st.indexOf(name)
        if arr:
            self.vm.writePop('temp', 0)
            self.vm.writePop('pointer', 1)
            self.vm.writePush('temp', 0)
            self.vm.writePop('that', 0)
        else: 
            self.vm.writePop(segment, index)

        self.file.write("</letStatement>\n")
        return

    def compileWhile(self):
        w = str(self.whiles)
        self.whiles += 1
        self.file.write("<whileStatement>\n")
        self.vm.writeLabel("LOOP." + w)
        self.writeAtom() #while
        self.writeAtom() #(
        self.compileExpression() #exp
        self.vm.writeArithmetic('~')
        self.writeAtom() #)
        self.writeAtom() #{
        self.vm.writeIf("END_OF_LOOP." + w)
        self.compileStatements() #statements
        self.vm.writeGoto("LOOP."+w)
        self.writeAtom() #}
        self.vm.writeLabel("END_OF_LOOP." + w)
        self.file.write("</whileStatement>\n")
        return

    def compileReturn(self):
        self.file.write("<returnStatement>\n")
        self.writeAtom() # return
        if (self.current.split()[1] != ';'):
            self.compileExpression()
        else:
            self.vm.writePush("constant", 0)
        self.writeAtom() #;
        self.file.write("</returnStatement>\n")
        self.vm.writeReturn();
        return

    def compileIf(self):
        f = str(self.ifs)
        self.ifs += 1
        self.file.write("<ifStatement>\n")
        self.writeAtom() #if
        self.writeAtom() #(
        self.compileExpression() #exp
        self.vm.writeArithmetic('~')
        self.writeAtom() #)
        self.vm.writeIf("IF_FALSE." + f)
        self.writeAtom() #{
        self.compileStatements()#statements
        self.writeAtom() #}

        e = self.current.split()[1] == 'else'
        if e:
            self.vm.writeGoto("END_OF_IF." + f)
            self.vm.writeLabel('IF_FALSE.' + f)
            self.writeAtom() #else
            self.writeAtom() #{
            self.compileStatements()
            self.writeAtom() #}
            self.vm.writeLabel("END_OF_IF." + f)
        else: 
            self.vm.writeLabel("IF_FALSE." + f)
       
        self.file.write("</ifStatement>\n")
        return

    def compileExpression(self):
        self.file.write("<expression>\n")
        self.compileTerm()
        while self.current.split()[1] in ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']:
            command = self.current.split()[1]
            self.writeAtom() #symbol
            self.compileTerm() 
            self.vm.writeArithmetic(command)

        self.file.write("</expression>\n")
        return

    def compileTerm(self):
        self.file.write("<term>\n")

        pos = self.tokens.tell()
        nextsym =self.tokens.readline().split()[1]
        self.tokens.seek(pos)

        first = self.current.split()[1]
        if (first == '-') | (first == '~'):
            if first == '-': first = 'neg'
            self.writeAtom() # - or ~
            self.compileTerm()
            self.vm.writeArithmetic(first)
        elif first == '(':
            self.writeAtom() # (
            self.compileExpression()
            self.writeAtom() # )
        elif nextsym == '[':
            name = self.current.split()[1]
            segment = self.st.kindOf(name)
            index = self.st.indexOf(name)
            
            self.writeAtom() # varName
            self.writeAtom() # [
            self.compileExpression()
            self.writeAtom() # ]
            self.vm.writePush(segment, index)
            self.vm.writeArithmetic('+')
            self.vm.writePop('pointer', 1)
            self.vm.writePush('that', 0)
        elif (nextsym == '(') | (nextsym == '.'):
            self.compileSubroutineCall()
        else:

            if self.current.split()[0] == "stringConstant":
                s = self.current[15:-1]
                self.vm.writePush("constant", len(s))
                self.vm.writeCall("String.new", 1)
                for x in range(len(s)):
                    num = ord(s[x])
                    self.vm.writePush("constant", num)
                    self.vm.writeCall("String.appendChar", 2)
            else:
                key = self.current.split()[1]
                segment = self.st.kindOf(key)
                if (segment == "NONE"):
                    segment = "constant"
                    if key == "true":
                        self.vm.writePush(segment, 0)
                        self.vm.writeArithmetic('~')
                    elif key == 'false':
                        index = 0
                    elif key == 'this':
                        segment = 'pointer'
                        index = 0
                    else:
                        index = key
                else:
                    index = self.st.indexOf(key)

                if key != "true":
                    self.vm.writePush(segment, index)


            self.writeAtom() #int string or keyword

        self.file.write("</term>\n")
        return
    
    def compileSubroutineCall(self):
        
        pos = self.tokens.tell()
        nextsym =self.tokens.readline().split()[1]
        self.tokens.seek(pos)
        
        name = ''
        if nextsym == '.':
            name = self.current.split()[1]
            segment = self.st.kindOf(name)
            if segment != "NONE":
                index = self.st.indexOf(name)
                self.vm.writePush(segment, index)
                name = self.st.typeOf(name)
                nArgs = 1
            else: nArgs = 0
            name += '.'
            self.writeAtom()#className or varName
            self.writeAtom() #.
        else: 
            name = self.ccname + '.'
            self.vm.writePush('pointer', 0)
            nArgs = 1
        name = name + self.current.split()[1]
        self.writeAtom() #subroutine name
        self.writeAtom() #(
        nArgs += self.compileExpressionList()
        self.writeAtom() #)
        self.vm.writeCall(name, nArgs)
        return

    def compileExpressionList(self):
        self.file.write("<expressionList>\n")
        nArgs = 0
        if self.current.split()[1] != ")":
            nArgs = 1
            self.compileExpression() #expression
            while(self.current.split()[1]==','):
                nArgs += 1
                self.writeAtom() #,
                self.compileExpression() #expression
        self.file.write("</expressionList>\n")

        return nArgs

    def writeAtom(self):
        if self.current.split()[0] == "stringConstant":
            tag = "stringConstant"
            tokey = self.current[15:-1]
        else:
            tag = self.current.split()[0]
            tokey = self.current.split()[1]
        
        self.file.write("<" + tag + "> " + tokey + " </" + tag + ">\n")
        self.current = self.tokens.readline()
        
        self.line+=1
        



