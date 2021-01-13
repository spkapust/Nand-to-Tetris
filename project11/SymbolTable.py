class SymbolTable:

    def __init__(self):
        self.subTable = {}
        self.classTable = {}
        return

    def startSubroutine(self):
        self.subTable = {}

    def define(self, name, type, kind):
        #if (kind == 'static') & (name in self.classTable): return
        i = 0
        if ((kind == 'field') | (kind == 'static')):
            for key in self.classTable:
                if (self.classTable[key]['kind'] == kind):
                    i += 1
            self.classTable[name] = {}
            self.classTable[name]['index'] = i
            self.classTable[name]['type'] = type
            self.classTable[name]['kind'] = kind
        else:
            for key in self.subTable:
                if (self.subTable[key]['kind'] == kind):
                    i += 1
            self.subTable[name] = {}
            self.subTable[name]['index'] = i
            self.subTable[name]['type'] = type
            self.subTable[name]['kind'] = kind
        return

    def varCount(self, kind):
        i = 0
        for key in self.subTable:
            if (self.subTable[key]['kind'] == kind):
                i += 1  
        for key in self.classTable:
            if (self.classTable[key]['kind'] == kind):
                i += 1     
        return i

    def kindOf(self, name):
        if name in self.subTable:
            return self.subTable[name]['kind']
        elif name in self.classTable:
            return self.classTable[name]['kind']
        else: 
            return "NONE"

    def typeOf(self, name):
        if name in self.subTable:
            return self.subTable[name]['type']
        else: 
            return self.classTable[name]['type']    

    def indexOf(self, name):
        if name in self.subTable:
            return self.subTable[name]['index']
        else: 
            return self.classTable[name]['index']  