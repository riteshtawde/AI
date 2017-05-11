'''
@author: ritesh(rtawde@iu.edu)
reference : http://artint.info/html/ArtInt_228.html
'''
class Solver:
    def __init__(self, mdp):
        self.mdp = mdp
        self.policy = dict([(state,'left') for state in self.mdp.S()])
        self.val = dict([(state, 0) for state in self.mdp.S()])
          
    def solve(self):
        return self.policy_iteration()
          
    def policy_iteration(self):
        val_changed = True
        while val_changed:
            val_changed = False
            self.policy_evaluation()
            for state in self.mdp.S():
                opt_pol = self.val[state]
                temp = 0
                for action in self.mdp.A():
                    temp = 0
                    for state_prime in self.mdp.S():
                        temp += self.mdp.P(state,action,state_prime) * (self.mdp.R(state_prime) + self.mdp.gamma()*self.val[state_prime])
                    if temp > opt_pol:
                        self.policy[state] = action
                        opt_pol = temp
                        val_changed = True
        return self.policy
    
    def policy_evaluation(self):
        for state in self.mdp.S():
            temp = 0
            for state_prime in self.mdp.S():
                temp += self.mdp.P(state,self.policy[state],state_prime) * (self.mdp.R(state_prime) + self.mdp.gamma()*self.val[state_prime])
            self.val[state] = temp