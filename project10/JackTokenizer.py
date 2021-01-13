class JackTokenizer:

    def __init__(self, file):
        self.file = open(file, 'r', encoding='utf-8')
        self.cc = ''
        self.token = ''
        self.type = ''
        self.keywords = {"class", "method", "function", "constructor", "int"  , "boolean", "char",
                         "void" , "var"   , "static"  , "field"      , "let"  , "do"     , "if"  ,
                         "else" , "while" , "return"  , "true"       , "false", "null"   , "this"}
        self.symbols = {'{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=', '~'}
        return

    def hasMoreTokens(self):
        pos = self.file.tell()
        c = self.file.read(1)

        while ((c == ' ') |( c == '\n' ) | (c =='\t') | ( c == '/')):
           
            #skip white space
            if ((c == ' ') | (c == '\n') | (c =='\t')):
                pos = self.file.tell()
                c=self.file.read(1)
        
            #skip all comments
            elif (c == '/'):
                c = self.file.read(1)
                if (c == '/'): 
                    while (c != '\n'): 
                        c = self.file.read(1)
                    pos = self.file.tell()
                    c = self.file.read(1)
                elif (c == '*'):
                    endComment = False
                    while (not endComment): 
                        c = self.file.read(1)
                        if (c == '*'):
                            c = self.file.read(1)
                            if (c == '/'):
                                endComment = True
                    pos = self.file.tell()
                    c = self.file.read(1)
                else:
                    self.file.seek(pos)
                    return True

        if not c: return False
        else: 
            self.file.seek(pos)
            return True

    def advance(self):
       self.cc = self.file.read(1)
       type = self.tokenType()
       if  (type == "KEYWORD"): 
           self.token = self.keyWord()
           self.type = "keyword"
       elif(type == "SYMBOL"): 
           self.token = self.symbol()
           self.type = "symbol"
       elif(type == "IDENTIFIER"): 
            self.token = self.identifier()
            self.type = "identifier"
       elif(type == "INT_CONST"): 
            self.token = self.intVal()
            self.type = "integerConstant"
       elif(type == "STRING_CONST"):
            self.token = self.stringVal()
            self.type = "stringConstant"
       #print(type)
      # print(self.token)
       #if self.token == 'return':
          # x=5

    def tokenType(self):
        if self.cc in self.symbols: return "SYMBOL"
        elif self.cc in ['0','1','2','3','4','5','6','7','8','9']: return "INT_CONST"
        elif self.cc == "\"": return "STRING_CONST"
        else: 
            token=self.cc
            pos = self.file.tell()
            c = self.file.read(1)
            while( (c != ' ') & (c != '\n') & (c != '\t') & (c not in self.symbols) ):
                token = token + c
                c = self.file.read(1)
            self.file.seek(pos)
            if token in self.keywords: return "KEYWORD"
            else: return "IDENTIFIER"


    def keyWord(self):
        token=''
        c = self.cc
        startp = self.file.tell()
        while( (c != ' ') & (c != '\n') &  (c != '\t') & (c not in self.symbols) ):
            pos=self.file.tell()
            token = token + c
            c = self.file.read(1)
        self.file.seek(pos)
        return token

    def symbol(self):
        if self.cc == '<': self.cc = '&lt;' 
        if self.cc == '>': self.cc=  '&gt;'
        if self.cc == '&': self.cc=  '&amp;'
        return self.cc
    
    def identifier(self):
        token=''
        c = self.cc
        while( (c != ' ') & (c != '\n') &  (c != '\t') & (c not in self.symbols) ):
            pos = self.file.tell()
            token = token + c
            c = self.file.read(1)
        self.file.seek(pos)
        return token

    def intVal(self):
        token=''
        c = self.cc
        while( c in ['0','1','2','3','4','5','6','7','8','9']):
            token = token + c
            pos = self.file.tell()
            c = self.file.read(1)
        self.file.seek(pos)
        return token

    def stringVal(self):
        token=''
        c=self.file.read(1)
        while( c != '\"'):
            token = token + c
            c = self.file.read(1)
        return token
