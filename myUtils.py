class Entry:
    def __init__(self, predicate, arguments=[], positive=True):
        self.predicate = predicate
        self.arguments = arguments
        self.positive = positive

    def inverse(self):
        self.positive = not self.positive
        return self

    def __repr__(self):
        s = self.predicate
        if not self.positive:
            s += " not "
        s += ": "
        for argument in self.arguments:
            s += argument + " "
        return s

class SubRule:
    relation = "AND"

    def __init__(self, line):
        self.index = {}
        self.variables = {}
        for item in line:
            self.index[item.predicate] = item
            for v in item.arguments:
                self.variables[v] = None

    def __contains__(self, item):
        return item in self.index

    def __repr__(self):
        s = "| "
        for key in self.index:
            s += str(self.index[key]) + " "
        return s

class Rule:
    relation = "OR"

    def __init__(self, table):
        self.index = {}
        self.namespace = {}
        if "OR" in table:
            for line in table["OR"]:
                item = SubRule(line)
                predicates = item.index.keys()
                for p in predicates:
                    self.index[p] = item
        else:
            item = SubRule(table["AND"])
            predicates = item.index.keys()
            for p in predicates:
                self.index[p] = item

    def __contains__(self, predicate):
        return predicate in self.index

    def __repr__(self):
        s = self.relation + " "
        for key in self.index:
            s += str(self.index[key])+" "
        return s


class Query(Entry):
    pass
class Fact(Query):
    pass
class Clause(Entry):
    pass