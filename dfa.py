from collections import defaultdict


"""The Deterministic Finite Automaton Class
A DFA is specified with a five tuple (Q, Sigma, delta, q0, F) where
Q: a set of states
Sigma: the set of symbols
delta: the transition function delta(q, a) = q' where q in Q and a in Sigma,
passed in either as a function of q and a, or a dictionary with (q, a) as the key and q' as the value. This implementation always convert delta into a function during the initialization.
q0: the start state, q0 in Q
F: the accept states, F is a subset of Q
"""
class DFA(object):
  def __init__(self, Q, Sigma, delta, q0, F):
    assert len(Q) > 0 and len(Sigma) > 0 and q0 in Q
    self.Q = Q
    self.Sigma = Sigma
    self.delta = delta if type(delta) not in [dict, defaultdict] else lambda x: delta.get(x, None)
    self.q0 = q0
    self.F = F

  def accept(self, w):
    '''Returns true if w is accepted by the DFA, and false otherwise.
    '''
    curr_state = self.q0
    for curr_symbol in w:
      curr_state = self.delta((curr_state, curr_symbol))
    return curr_state in self.F
