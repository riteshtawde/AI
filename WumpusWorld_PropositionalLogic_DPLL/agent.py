'''
rtawde@iu.edu
'''
import pickle
from copy import deepcopy

class Percept:
    breeze = False
    stench = False
    
    def __init__(self, breeze, stench):
        self.breeze = breeze
        self.stench = stench
    
class Agent:
    xWidth = 0
    yWidth = 0
    maxRows = 20
    maxCols = 20
    sentences = []
    cnf = []
    literals = []
    percept = Percept(False, False)
    prev_location = []
    cur_row = -1
    cur_col = -1
    visited = []
    wumpus_dead = False
    breeze = False
    stench = False
    action = ''
    not_recom_move = []
    clause_copy = []
    literal_list = []
    atmost_one_wump = []
    
    
    def __init__(self):
        self.xWidth = 20
        self.yWidth = 20
        assert(self.xWidth <= self.maxRows and self.yWidth <= self.maxCols)
        self.buildInitialKnowledgeBase()
    
    def buildInitialKnowledgeBase(self):
        self.tell([{'-P11'}])
        self.tell([{'-W11'}])
                             
        #At Lest one Wumpus
        cnf= []
        for x in range(1,self.xWidth+1):
            for y in range(1,self.yWidth+1):
                temp = 'W'+str(x)+str(y)
                cnf.append(temp)
        self.tell([set(cnf)])
        
#         #At Most one Wumpus
#         cnf = []
#         grids = self.xWidth * self.yWidth
#         for i in range(grids):
#             for j in range(i+1, grids):
#                 first = 'W'+str(int(i/self.xWidth)+1)+str(int(i%self.yWidth)+1) 
#                 second = 'W'+str(int(j/self.xWidth)+1)+str(int(j%self.yWidth)+1)
#                 temp2 = ['-'+first,'-'+ second]
#                 self.tell([set(temp2)])      
                    
    def build_kb(self):
        x = self.cur_row
        y = self.cur_col
        if x > 0 and  y > 0:
            self.tell([set(['-B'+str(x)+str(y),'P'+str(x+1)+str(y),'P'+str(x-1)+str(y),'P'+str(x)+str(y+1),'P'+str(x)+str(y-1)])])
            self.tell([set(['-P'+str(x+1)+str(y),'B'+str(x)+str(y)])])
            self.tell([set(['-P'+str(x-1)+str(y),'B'+str(x)+str(y)])])
            self.tell([set(['-P'+str(x)+str(y+1),'B'+str(x)+str(y)])])
            self.tell([set(['-P'+str(x)+str(y-1),'B'+str(x)+str(y)])])
            
            self.tell([set(['-S'+str(x)+str(y),'W'+str(x+1)+str(y),'W'+str(x-1)+str(y),'W'+str(x)+str(y+1),'W'+str(x)+str(y-1)])])
            self.tell([set(['-W'+str(x+1)+str(y),'S'+str(x)+str(y)])])
            self.tell([set(['-W'+str(x-1)+str(y),'S'+str(x)+str(y)])])
            self.tell([set(['-W'+str(x)+str(y+1),'S'+str(x)+str(y)])])
            self.tell([set(['-W'+str(x)+str(y-1),'S'+str(x)+str(y)])])
        temp = []
        temp.append('-W'+str(x+1)+str(y))
        temp.append('-W'+str(x-1)+str(y))
        temp.append('-W'+str(x)+str(y+1))
        temp.append('-W'+str(x)+str(y-1))
        
        clause_list = []    
        for each in temp:
            for another in temp:
                if each != another:
                    clause = {each, another}
                    if clause not in clause_list:
                        self.tell([set([each, another])])
                    if each not in self.atmost_one_wump:
                        self.atmost_one_wump.append(each)
        #print(self.atmost_one_wump)
        for each in temp:
            for i in self.atmost_one_wump:
                if each != i:
                    if {each, i} not in self.cnf:
                        self.tell([set([each, i])])
    
    def makePerceptSentence(self, percept, x, y):
        temp = 'B'+str(x)+str(y)
        if percept.breeze:
            self.tell([set([temp])])
        else:
            temp = '-'+temp
            self.tell([set([temp])])
        
        temp = 'S'+str(x)+str(y)
        if percept.stench:
            self.tell([set([temp])])
            self.build_kb()
        else:
            temp = '-'+temp
            self.tell([set([temp])])
                    
    def tell(self, cnf):
        for i in cnf:
            if i not in self.cnf:
                self.cnf.append(i)
    def tell_wump(self,cnf):
        for i in cnf:
            if i not in self.cnf_wump:
                self.cnf_wump.append(i) 
                    
    def get_action(self):
        self.makePerceptSentence(self.percept, self.cur_row, self.cur_col)
        
        #print(self.cnf)
        
        #Right
        if  [self.cur_row+1,self.cur_col] not in self.visited and [self.cur_row+1,self.cur_col] not in self.not_recom_move:
            if self.stench or self.breeze:
                self.action = self.try_move(self.cur_row+1, self.cur_col)
                if self.action == True:
                    self.action = 'MOVE_RIGHT'
                    return self.action
                if self.action == 'KILL':
                    self.action = 'SHOOT_RIGHT'
                    return self.action
            else:
                self.action = 'MOVE_RIGHT'
                return self.action
        
        #Left
        if [self.cur_row-1,self.cur_col] not in self.visited and [self.cur_row-1, self.cur_col] not in self.not_recom_move:
            if  self.stench or self.breeze:
                self.action = self.try_move(self.cur_row-1, self.cur_col)
                if self.action == True:
                    self.action = 'MOVE_LEFT'
                    return self.action
                if self.action == 'KILL':
                    self.action = 'SHOOT_LEFT'
                    return self.action
            else:
                self.action = 'MOVE_LEFT'
                return self.action
        #Up
        if [self.cur_row,self.cur_col+1] not in self.visited and [self.cur_row, self.cur_col+1]  not in self.not_recom_move:
            if self.stench or self.breeze:
                self.action = self.try_move(self.cur_row, self.cur_col+1)
                if self.action == True:
                    self.action = 'MOVE_UP'
                    return self.action
                if self.action == 'KILL':
                    self.action = 'SHOOT_UP'
                    return self.action
            else:
                self.action = 'MOVE_UP'
                return self.action
        #Down
        if [self.cur_row,self.cur_col-1] not in self.visited and [self.cur_row, self.cur_col-1]  not in self.not_recom_move:
            if self.stench or self.breeze:
                self.action = self.try_move(self.cur_row, self.cur_col-1)
                if self.action == True:
                    self.action = 'MOVE_DOWN'
                    return self.action
                if self.action == 'KILL':
                    self.action = 'SHOOT_DOWN'
                    return self.action    
            else:
                self.action = 'MOVE_DOWN'
                return self.action
        return self.backtrack_move()
        
    def backtrack_move(self):
        if self.prev_location:
            pop_prev = self.prev_location.pop()
            if not self.prev_location:
                return 'QUIT'
            elif self.checkListEquality(pop_prev, [self.cur_row, self.cur_col]):
                pop_prev = self.prev_location.pop()
                if pop_prev[0] > self.cur_row:
                    return 'MOVE_RIGHT'
                elif pop_prev[0] < self.cur_row:
                    return 'MOVE_LEFT'
                elif pop_prev[1] > self.cur_col:
                    return 'MOVE_UP'
                elif pop_prev[1] < self.cur_col:
                    return 'MOVE_DOWN'
        else:
            return 'QUIT'
    
    def try_move(self, x, y):
        pit_n_wumpus = False
        pit = False
        wumpus = False
        if not self.wumpus_dead:
            pit_n_wumpus = self.ask({'W'+str(x)+str(y),'P'+str(x)+str(y)})
        else:
            pit_n_wumpus = self.ask({'P'+str(x)+str(y)})
        if not pit_n_wumpus:
            return True
        else:
            pit = self.ask({'-P'+str(x)+str(y)})
            if not pit:
                temp = 'P'+str(x)+str(y)
                self.tell([set([temp])])
            if not self.wumpus_dead:
                wumpus = self.ask({'-W'+str(x)+str(y)})
                if not wumpus:
                    return 'KILL'
        return False
    
    def ask(self, clause):
        #cnf_copy.append(pickle.loads(pickle.dumps(self.cnf, -1)))
        cnf_copy = deepcopy(self.cnf)
        cnf_copy.append(clause)
        #print('cnf before ask : ',cnf_copy)
        #cnf_copy.append(clause)
        self.clause_copy = []
        self.literal_list = []
        if self.dpllSolve(cnf_copy):
            return True
        return False
    
    def killed_wumpus(self):
        self.wumpus_dead = True
    
    def checkListEquality(self,x, y):
        return x[0] == y[0] and x[1] == y[1] 
        
    def give_senses(self, location, breeze, stench):
        self.breeze = breeze
        self.stench = stench
        #compare lists
        temp = []
        temp.append(self.cur_row)
        temp.append(self.cur_col)
        if self.checkListEquality(location, temp):
            if self.action == 'MOVE_LEFT':
                self.not_recom_move.append([location[0]-1, location[1]])
            elif self.action == 'MOVE_RIGHT':
                self.not_recom_move.append([location[0]+1, location[1]])
            elif self.action == 'MOVE_UP':
                self.not_recom_move.append([location[0], location[1]+1])
            elif self.action == 'MOVE_DOWN':
                self.not_recom_move.append([location[0], location[1]-1])
        else:
            self.prev_location.append([location[0], location[1]])
            self.visited.append([location[0], location[1]])
            self.cur_row = location[0]
            self.cur_col = location[1]
        self.percept = Percept(self.breeze, self.stench)
    
    def dpllSolve(self, clause):
        if clause.__len__() == 0:
            return True
        elif self.containsEmptySet(clause):
            return False
        else:
            unit = self.getUnitClause(clause)
            if unit != 0 and self.dpllSolve(self.unitPropogation(clause, unit, True)):
                return True
            #print('before pure : ',clause)
            unit = self.getPureLiteral(clause)
            if unit != 0 and not self.containsEmptySet(clause) and self.dpllSolve(self.unitPropogation(clause, unit, True)):
                return True
            unit = self.getFirstLiteral(clause)
            
            #self.clause_copy.append(deepcopy(clause))
            #self.literal_list.append(unit)
            if unit != 0 and not self.containsEmptySet(clause) and self.dpllSolve(self.unitPropogation(clause, unit, True)):
                return True
            else:
                clause = self.clause_copy.pop()
                #print(self.literal_list)
                unit = self.literal_list.pop()
                return self.dpllSolve(self.unitPropogation(clause, self.negateClause(unit), False))

                
        
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

    def unitPropogation(self, clause, literal, condition):
        if condition:
            self.clause_copy.append(pickle.loads(pickle.dumps(clause, -1)))
            self.literal_list.append(literal)
        i=0
        while(i<clause.__len__()):
            #print('clause : ',clause)
            for j in clause[i]:
                if j == literal:
                    clause.remove(clause[i])
                    i-=1
                    break
                elif j == self.negateClause(literal):
                    clause[i].remove(j)
                    break
            i+=1
        return clause

    def getPureLiteral(self, clause):
        union_set = set()
        for i in clause:
            #print(union_set,' | ',i)
            union_set = union_set | i
        
        #print(union_set)    
        
        for i in union_set:
            if self.negateClause(i) in union_set:
                continue
            return i
        return 0
                
    def getFirstLiteral(self, clause):
        for i in clause:
            if not i== set():
                for j in i:
                    return j 
        return 0
    
    def negateClause(self, i):
        if i[0] == '-':
            return i[1:]
        else:
            return '-' + i