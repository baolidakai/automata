from dfa import *
from nfa import *

# Utility functions
def BFS(start_state, Sigma, delta):
  '''Return the states visited by traversing through symbols in Sigma from start_state, using delta transition function.
  '''
  visited = {start_state}
  frontier = [start_state]
  while frontier:
    next_frontier = []
    for curr in frontier:
      # Get all unvisited neighbors
      for symb in Sigma:
        candidate = delta((curr, symb))
        if candidate not in visited:
          visited.add(candidate)
          next_frontier.append(candidate)
    frontier = next_frontier
  return visited

def table_filling(states, accept_states, reject_states, Sigma, delta):
  '''Returns the table filled given the accept/reject states, symbols and transitions.
  '''
  table = set()
  for accept_state in accept_states:
    for reject_state in reject_states:
      table.add((accept_state, reject_state))
      table.add((reject_state, accept_state))
  terminated = False
  while not terminated:
    # Iterate through all states and symbols
    terminated = True
    for state1 in states:
      for state2 in states:
        for symb in Sigma:
          if (state1, state2) not in table and state1 != state2:
            if (delta((state1, symb)), delta((state2, symb))) in table:
              table.add((state1, state2))
              table.add((state2, state1))
              terminated = False
  return table

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

def DFA2MIN(D):
  '''Return an equivalent DFA with minimum number of states.
  Remove inaccessible states.
  Use table-filling algorithm to group states.
  Q' = {[q]}
  q0' = [q0]
  F' = {[q]|q in F}
  delta'([q], sigma) = [delta(q, sigma)]

  Table-filling algorithm: mark all accept/reject pairs
  if any p, q, sigma, s.t. (delta(p, sigma), delta(q, sigma)) marked, mark p, q
  repeat until no new pairs
  '''
  # Remove inaccessible states by getting all reachable states using BFS
  states = BFS(D.q0, D.Sigma, D.delta)
  # Table-filling algorithm to mark all distinguishable pairs of states
  table = table_filling(states, states & D.F, states - D.F, D.Sigma, D.delta)
  group_ids = dict() # state => group_id
  group_representatives = [] # representative state for each group_id
  group_id = 0
  for state in states:
    if state not in group_ids:
      group_ids[state] = group_id
      group_representatives.append(state)
      for state2 in states:
        if state2 not in group_ids:
          if (state, state2) not in table:
            # state ~ state2
            group_ids[state2] = group_id
      group_id += 1
  # Q' = {[q]}
  min_Q = set(group_representatives)
  min_Sigma = D.Sigma
  # q0' = [q0]
  min_q0 = group_representatives[group_ids[D.q0]]
  # F' = {[q]|q in F}
  min_F = {group_representatives[group_ids[q]] for q in D.F}
  # delta'([q], sigma) = [delta(q, sigma)]
  min_delta = dict()
  for q in group_representatives:
    for symb in min_Sigma:
      neighbor = D.delta((q, symb))
      neighbor = group_representatives[group_ids[neighbor]]
      min_delta[(q, symb)] = neighbor
  return DFA(min_Q, min_Sigma, min_delta, min_q0, min_F)
