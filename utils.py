from dfa import *
from nfa import *

# Utility functions
def DFA2NFA(dfa1):
  # Convert dfa1 to an equivalent nfa
  delta = lambda x: set([dfa1.delta(x)]) if dfa1.delta(x) is not None else {}
  return NFA(dfa1.Q, dfa1.Sigma, delta, dfa1.q0, dfa1.F)

def NFA2DFA(N):
  # Convert nfa N to dfa D using subset construction
  # BFS from the start set
  initial_subset = tuple(sorted(N.get_epsilon_neighbors(N.q0)))
  visited = {initial_subset}
  frontier = [initial_subset]
  transitions = dict()
  final_states = set()
  while frontier:
    new_frontier = []
    for curr_subset in frontier:
      # delta'(R, sigma) is union of epsilon-transition of delta(r, sigma) for all r in R
      if N.F and curr_subset:
        final_states.add(curr_subset)
      for symbol in N.Sigma:
        next_subset = set()
        for r in curr_subset:
          # get epsilon(delta(r, sigma))
          for nbr in N.delta((r, symbol)):
            for state in N.get_epsilon_neighbors(nbr):
              next_subset.add(state)
        next_subset = tuple(sorted(next_subset))
        if next_subset not in visited:
          visited.add(next_subset)
          new_frontier.append(next_subset)
        transitions[(curr_subset, symbol)] = next_subset
    frontier = new_frontier
  return DFA(visited, N.Sigma, transitions, initial_subset, final_states)
