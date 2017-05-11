'''
rtawde@iu.edu
'''
import pickle
class Solver:
    def __init__(self, cnf):
        self.clause_list = cnf
        self.clause_copy = []
        self.literal_list = []
        
    def solve(self):
        return self.dpllSolve(self.clause_list)
        
    def dpllSolve(self, clause):
        if clause.__len__() == 0:
            return True
        elif self.containsEmptySet(clause):
            return False
        else:
            unit = self.getUnitClause(clause)
            if unit != 0 and self.dpllSolve(self.unitPropogation(clause, unit)):
                return True
            unit = self.getPureLiteral(clause)
            if unit != 0 and not self.containsEmptySet(clause) and self.dpllSolve(self.unitPropogation(clause, unit)):
                return True
            unit = self.getFirstLiteral(clause)
            self.clause_copy.append(pickle.loads(pickle.dumps(clause, -1)))
            self.literal_list.append(pickle.loads(pickle.dumps(unit, -1)))
            if unit != 0 and not self.containsEmptySet(clause) and self.dpllSolve(self.unitPropogation(clause, unit)):
                return True
            else:
                clause = self.clause_copy.pop()
                unit = self.literal_list.pop()
                return self.dpllSolve(self.unitPropogation(clause, -unit))

                
        
    def containsEmptySet(self, clause):
        for i in clause:
            if i == set():
                return True
        return False

    def getUnitClause(self, clause):
        for i in clause:
            if i.__len__() == 1:
                for j in i:
                    return j
        return 0

    def unitPropogation(self, clause, literal):
        i=0
        while(i<clause.__len__()):
            for j in clause[i]:
                if j == literal:
                    clause.remove(clause[i])
                    i-=1
                    break
                elif j == -literal:
                    clause[i].remove(j)
                    break
            i+=1
        return clause

    def getPureLiteral(self, clause):
        union_set = set()
        for i in clause:
            #print(union_set,' | ',i)
            union_set = union_set | i

        for i in union_set:
            if -i in union_set:
                continue
            return i
        return 0
                
    def getFirstLiteral(self, clause):
        for i in clause:
            if not i== set():
                for j in i:
                    return j 
        return 0