'''
@author: ritesh(rtawde@iu.edu)
'''
import solver
import time
class WumpusMDP:
    # wall_locations is a list of (x,y) pairs
    # pit_locations is a list of (x,y) pairs
    # wumnpus_location is an (x,y) pair
    # gold_location is an (x,y) pair
    # start_location is an (x,y) pair representing the start location of the agent
    
    states = []
    #change dimensions here as per the input to constructor 
    grid_dimension_x = 5
    grid_dimension_y = 6
    wumpus_dead = False
    has_arrow = True
    
    def __init__(self, wall_locations, pit_locations, wumpus_location, gold_location, start_location):
        self.wall_locations = wall_locations
        self.pit_locations = pit_locations
        self.wumpus_location = wumpus_location
        self.gold_location = gold_location
        self.start_location = start_location
        for x in range(self.grid_dimension_x):
            for y in range(self.grid_dimension_y):
                if (x,y) not in self.wall_locations:
                    self.states.append((x,y))   
    
    def A(self):
        return ['do nothing','left','right','up','down','shoot left','shoot right','shoot up','shoot down']
    
    def S(self):
        return self.states
        
    def P(self, s, a, u):
        if (a == 'up' or a == 'down' or a == 'left' or a == 'right') and u in self.wall_locations:
            return 0        
        if a == 'do nothing' and s == u and s == self.gold_location:
            return 1 
        
        if a == 'up' and u[1] == s[1]+1 and u[0] == s[0]:
            return 0.9
        if a == 'up' and self.in_neighbour_states(s, u):
            return 0.1/3     
        if a == 'shoot up' and s[0] == self.wumpus_location[0] and s[1] < self.wumpus_location[1] and not self.wumpus_dead and self.has_arrow and s==u:
            self.wumpus_dead = True
            self.has_arrow = False
            return 1
        #down
        if a == 'down' and u[1] == s[1]-1 and u[0] == s[0]:
            return 0.9
        if a == 'down' and self.in_neighbour_states(s, u):
            return 0.1/3            
        if a == 'shoot down' and s[0] == self.wumpus_location[0] and s[1] > self.wumpus_location[1] and not self.wumpus_dead and self.has_arrow  and s==u:
            self.wumpus_dead = True
            self.has_arrow = False
            return 1
        
        #left
        if a == 'left' and u[0] == s[0]-1 and u[1] == s[1]:
            return 0.9
        if a == 'left' and self.in_neighbour_states(s, u):
            return 0.1/3
        if a == 'shoot left' and s[1] == self.wumpus_location[1] and s[0] > self.wumpus_location[0] and not self.wumpus_dead and self.has_arrow  and s==u:
            self.wumpus_dead = True
            self.has_arrow = False
            return 1
        
        #right
        if a == 'right' and u[0] == s[0]+1 and u[1] == s[1]:
            return 0.9
        if a == 'right' and self.in_neighbour_states(s, u):
            return 0.1/3
        if a == 'shoot right' and s[1] == self.wumpus_location[1] and s[0] < self.wumpus_location[0] and not self.wumpus_dead and self.has_arrow  and s==u:
            self.wumpus_dead = True
            self.has_arrow = False
            return 1
        return 0
        
    def R(self, s):
        if s == self.wumpus_location and not self.wumpus_dead:
            return -100
        elif  s in self.pit_locations:
            return -100
        elif s == self.gold_location:
            return 100
        return -1
    
    def initial_state(self):
        return self.start_location
    
    def gamma(self):
        return 0.99
    
    def in_neighbour_states(self, state, neighbour):
        return True if ((neighbour[0] == state[0]-1 or neighbour[0] == state[0]+1)  and neighbour[1] == state[1] ) or ((neighbour[1] == state[1]-1 or neighbour[1] == state[1]+1) and neighbour[0] == state[0]) else False

#mdp = WumpusMDP([(0,0),(1,0),(2,0),(3,0),(3,1),(3,2),(3,3),(2,3),(1,3),(0,3),(0,2),(0,1)], [(1,2)], (2,1), (2,2), (1,1)) 
mdp = WumpusMDP([(0,0),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(3,5),(2,5),(1,5),(0,5),(0,4),(0,3),(0,2),(0,1),(2,3)], [(1,2)], (3,2), (3,4), (1,1))
solve = solver.Solver(mdp)
start = time.time()
policy = solve.solve()
end = time.time()
#print('time : ',(end-start))
print(policy)