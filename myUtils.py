from collections import deque


class Query:
    def __init__(self):
        self.clauses = []
        self.theta = {}
        self.information = None
        self.variables = set()

    def done(self):
        for clause in self.clauses:
            for arg in clause.arguments:
                if arg not in self.theta and arg not in self.variables:
                    self.variables.add(arg)
                    self.theta[arg] = []
        s = str(self.clauses) + " theta:  " + str(self.theta)
        self.information = s

    def __repr__(self):
        return self.information

    def __hash__(self):
        return hash(self.information)


class Rule:
    def __init__(self, line):
        self.index = {}
        self.clauses = line
        for clause in line:
            if clause not in self.index:
                self.index[clause.predicate] = []
            else:
                print("DAMN!")
            self.index[clause.predicate].append(clause)

    def __contains__(self, item):
        return item in self.index

    def __repr__(self):
        return str(self.index)


class MyQueue:
    def __init__(self):
        self.queue = deque()

    def push(self, item):
        self.queue.append(item)

    def pop(self):
        return self.queue.popleft()

    def size(self):
        return len(self.queue)

    def __repr__(self):
        s = "Queue: "
        for item in self.queue:
            s += str(item)
        return s


class Entry:
    def __init__(self, predicate, arguments=[], positive=True):
        self.predicate = predicate
        self.arguments = arguments
        self.positive = positive
        self.theta = None
        self.info = None

    def inverse(self):
        self.positive = not self.positive
        return self

    def __repr__(self):
        if self.info:
            return self.info
        s = self.predicate
        if not self.positive:
            s += " not "
        s += ": "
        for argument in self.arguments:
            s += argument + " "
        self.info = s
        return s

class Fact(Entry):
    pass


class Clause(Entry):
    pass

