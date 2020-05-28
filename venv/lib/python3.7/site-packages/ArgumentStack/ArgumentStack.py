
class ArgumentStack(object):
    
    def __init__(self, error_msg=""):
        self.stack = []
        self.types = [] 
        self.error_msg = error_msg

        # in types:
        # 0 - command 
        # 1 - value 

        self.actions = [] # list of tuples where first tuple is a stack and second is function, third is help

    def pushCommand(self, cmd):
        self.stack.append(cmd)
        self.types.append(0)

    def pushVariable(self, var_name):
        self.stack.append(var_name)
        self.types.append(1)

    def pop(self):
        self.stack = self.stack[:-1]
        self.types = self.types[:-1]

    def popAll(self):
        self.stack = [] 
        self.types = []

    def assignAction(self, func, help=""):
        l = [] 
        for i in range(len(self.stack)):
            if self.types[i] == 0:
                l.append(self.stack[i])
            else:
                l.append("*" + self.stack[i])
        self.actions.append((l, func, help))

    def getHelp(self):
        s = ""
        for a in self.actions:
            clear = [] 
            for e in a[0]:
                if "*" in e[0]:
                    clear.append("<" + e[1:].upper() + ">")
                else:
                    clear.append(e)
            s +="\t%s \t\t\t %s\n" % (" ".join(clear), a[2])
        return s

    def execute(self, args):
        """
        Here 0th argument (args[0]) is the name of the program
        """
        params = {}
        for action in self.actions:
            found = True
            l = action[0]
            if len(l)+1 == len(args):
                for i in range(len(l)):
                    if l[i][0] != "*" and l[i] != args[i+1]:
                        found = False 
                    if l[i][0] == "*":
                        params[l[i][1:]] = args[i+1]
                if found:
                    action[1](**params)
                    return
        print(self.error_msg)
