class Memory:
    def __init__(self, name): # memory name
        self.memory = {}

    def has_key(self, name): # variable name
        return name in self.memory.keys()

    def get(self, name): # gets from memory current value of variable <name>
        return self.memory.get(name, None)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memory.update({name: value})


class MemoryStack:                                     
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        if memory is None:
            self.stack = [Memory("Nothing - init")]
        else:
            self.stack = [memory]

    def get(self, name): # gets from memory stack current value of variable <name>
        for m in self.stack:
            res = m.get(name)
            if res is not None:
                return res

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[0].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for stack in self.stack:
            if stack.has_key(name):
                return stack.put(name, value)
        self.insert(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.stack.insert(0, Memory("Nothing - Push"))

    def pop(self): # pops the top memory from the stack
        self.stack.pop(0)


