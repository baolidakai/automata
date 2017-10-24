from collections import defaultdict


"""The Nondeterministic Finite Automaton Class
A NFA is specified with a five tuple (Q, Sigma, delta, q0, F) where
Q: a set of states
Sigma: the set of symbols
delta: the transition function delta(q, a) = subset of Q where q in Q and a in Sigma,
passed in either as a function of q and a, or a dictionary with (q, a) as the key and the subset as the value. This implementation always convert delta into a function during the initialization. a could be '' representing epsilon.
q0: the start state, q0 in Q
F: the accept states, F is a subset of Q
"""
class NFA(object):
  def __init__(self, Q, Sigma, delta, q0, F):
    assert len(Q) > 0 and len(Sigma) > 0 and q0 in Q
    self.Q = Q
    self.Sigma = Sigma
    self.delta = delta if type(delta) not in [dict, defaultdict] else lambda x: delta.get(x, {})
    self.q0 = q0
    self.F = F
    # epsilon_neighbors[q] computes and caches the neighborhood of q with only epsilon out paths
    self.epsilon_neighbors = dict()

  def get_epsilon_neighbors(self, q):
    '''Return the neighbors of q including q itself
    with only epsilon out links. Use cached result if that exists.
    '''
    if q in self.epsilon_neighbors:
      return self.epsilon_neighbors[q]
    # Run a breadth first search
    neighborhood = {q}
    frontier = [q]
    while frontier:
      new_frontier = []
      for curr in frontier:
        # Enqueue all unvisited neighbors of curr
        for neighbor in self.delta((curr, '')):
          if neighbor not in neighborhood:
            new_frontier.append(neighbor)
            neighborhood.add(neighbor)
      frontier = new_frontier
    self.epsilon_neighbors[q] = neighborhood
    return neighborhood

  def accept(self, w):
    '''Returns true if w is accepted by the NFA, and false otherwise.
    '''
    # curr_states stores all possible states in all possible branches
    curr_states = self.get_epsilon_neighbors(self.q0)
    for symbol in w:
      # Update the next states one step from current states
      next_states = set()
      for curr_state in curr_states:
        for next_state in self.delta((curr_state, symbol)):
          next_states |= self.get_epsilon_neighbors(next_state)
      curr_states = next_states
    # accept if any acceptable state is reached
    return curr_states & self.F
