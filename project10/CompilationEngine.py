import os

class CompilationEngine:

    def __init__(self, tokens, file):
        self.tokens = tokens
        self.file = file
        self.line = 1
        self.current = self.tokens.readline()
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
        return

    def compileClassVarDec(self):
        self.file.write("<classVarDec>\n")
        self.writeAtom() #static or field
        self.writeAtom() #type
        self.writeAtom() # varName
        while(self.current.split()[1] != ';'):
            self.writeAtom() #,
            self.writeAtom() #varName
        self.writeAtom() #;
        self.file.write("</classVarDec>\n")
        return

    def compileSubroutine(self):
        self.file.write("<subroutineDec>\n")
        self.writeAtom() #constructor, function, or method
        self.writeAtom() #void or type
        self.writeAtom() #subRoutine Name
        self.writeAtom() #(
        self.compileParameterList()
        self.writeAtom() #)
        
        self.file.write("<subroutineBody>\n")
        self.writeAtom() #{
        while(self.current.split()[1] == 'var'):
            self.compileVarDec()
        while(self.current.split()[1] in ['let', 'if', 'while', 'do', 'return']):
            self.compileStatements()
        self.writeAtom() #}
        self.file.write("</subroutineBody>\n")

        self.file.write("</subroutineDec>\n")
        return

    def compileParameterList(self):
        self.file.write("<parameterList>\n")
        if self.current.split()[0] != 'symbol':
            self.writeAtom() #type
            self.writeAtom() #varName
            while(self.current.split()[1] == ','):
                self.writeAtom() #,
                self.writeAtom() #type
                self.writeAtom() #varName
        self.file.write("</parameterList>\n")
        return

    def compileVarDec(self):
        self.file.write("<varDec>\n")
        self.writeAtom() #var
        self.writeAtom() #type
        self.writeAtom() #varname
        while(self.current.split()[1] != ';'):
            self.writeAtom() #,
            self.writeAtom() #varName
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
        return

    def compileLet(self):
        self.file.write("<letStatement>\n")
        self.writeAtom() #let
        self.writeAtom() #varName
        if(self.current.split()[1] == '['):
            self.writeAtom() #[
            self.compileExpression() #expression
            self.writeAtom() #]
        self.writeAtom() #=
        self.compileExpression() #expression
        self.writeAtom() #;
        self.file.write("</letStatement>\n")
        return

    def compileWhile(self):
        self.file.write("<whileStatement>\n")
        self.writeAtom() #while
        self.writeAtom() #(
        self.compileExpression() #exp
        self.writeAtom() #)
        self.writeAtom() #{
        self.compileStatements() #statements
        self.writeAtom() #}
        self.file.write("</whileStatement>\n")
        return

    def compileReturn(self):
        self.file.write("<returnStatement>\n")
        self.writeAtom() # return
        if (self.current.split()[1] != ';'):
            self.compileExpression()
        self.writeAtom() #;
        self.file.write("</returnStatement>\n")
        return

    def compileIf(self):
        self.file.write("<ifStatement>\n")
        self.writeAtom() #if
        self.writeAtom() #(
        self.compileExpression() #exp
        self.writeAtom() #)
        self.writeAtom() #{
        self.compileStatements()#statements
        self.writeAtom() #}
        if self.current.split()[1] == 'else':
            self.writeAtom() #else
            self.writeAtom() #{
            self.compileStatements()
            self.writeAtom() #}
        self.file.write("</ifStatement>\n")
        return

    def compileExpression(self):
        self.file.write("<expression>\n")
        self.compileTerm()
        while self.current.split()[1] in ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']:
            self.writeAtom() #symbol
            self.compileTerm() 
        self.file.write("</expression>\n")
        return

    def compileTerm(self):
        self.file.write("<term>\n")

        pos = self.tokens.tell()
        nextsym =self.tokens.readline().split()[1]
        self.tokens.seek(pos)

        first = self.current.split()[1]
        if (first == '-') | (first == '~'):
            self.writeAtom() # - or ~
            self.compileTerm()
        elif first == '(':
            self.writeAtom() # (
            self.compileExpression()
            self.writeAtom() # )
        elif nextsym == '[':
            self.writeAtom() # varName
            self.writeAtom() # [
            self.compileExpression()
            self.writeAtom() # ]
        elif (nextsym == '(') | (nextsym == '.'):
            self.compileSubroutineCall()
        else:
            self.writeAtom() #int string or keyword

        self.file.write("</term>\n")
        return
    
    def compileSubroutineCall(self):
        
        pos = self.tokens.tell()
        nextsym =self.tokens.readline().split()[1]
        self.tokens.seek(pos)
        
        if nextsym == '.':
            self.writeAtom()#className or varName
            self.writeAtom() #.
        self.writeAtom() #subroutine name
        self.writeAtom() #(
        self.compileExpressionList()
        self.writeAtom() #)
        return

    def compileExpressionList(self):
        self.file.write("<expressionList>\n")
        if self.current.split()[1] != ")":
            self.compileExpression() #expression
            while(self.current.split()[1]==','):
                self.writeAtom() #,
                self.compileExpression() #expression
        self.file.write("</expressionList>\n")

            

        return

    def writeAtom(self):
        words = self.current.split()
        for i in range(2, len(words)):
            words[1] = words[1] + ' ' + words[i]
        self.file.write("<" + words[0] + "> " + words[1] + " </" + words[0] + ">\n")
        self.current = self.tokens.readline()
        #wtf = self.tokens.tell()
        self.line+=1
        if words[1] == 'drawRectangle':
            u=2


