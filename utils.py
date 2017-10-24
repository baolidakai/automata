from dfa import *
from nfa import *

# Utility functions
def DFA2NFA(dfa1):
  # Convert dfa1 to an equivalent nfa
  delta = lambda x: set([dfa1.delta(x)]) if dfa1.delta(x) is not None else {}
  return NFA(dfa1.Q, dfa1.Sigma, delta, dfa1.q0, dfa1.F)
