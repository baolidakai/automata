from nfa import *
# Tests for the NFA class

# Functionality of get_epsilon_neighbors
nfa_1 = NFA(
    {'q1', 'q2', 'q3', 'q4'},
    {'0'},
    {
      ('q1', ''): {'q2', 'q3', 'q4'},
      ('q2', ''): {'q1', 'q3'}
    },
    'q1',
    {'q4'}
    )

assert nfa_1.get_epsilon_neighbors('q1') == {'q1', 'q2', 'q3', 'q4'}
assert nfa_1.get_epsilon_neighbors('q2') == {'q1', 'q2', 'q3', 'q4'}
assert nfa_1.get_epsilon_neighbors('q3') == {'q3'}
assert nfa_1.get_epsilon_neighbors('q4') == {'q4'}

# example 1.30
nfa_1_30 = NFA(
    {'q1', 'q2', 'q3', 'q4'},
    {'0', '1'},
    {
      ('q1', '0'): {'q1'},
      ('q1', '1'): {'q1', 'q2'},
      ('q2', '0'): {'q3'},
      ('q2', '1'): {'q3'},
      ('q3', '0'): {'q4'},
      ('q3', '1'): {'q4'}
    },
    'q1',
    {'q4'}
    )

assert nfa_1_30.accept('000100')
assert not nfa_1_30.accept('0011')

# example 1.35
nfa_1_35 = NFA(
    {'q1', 'q2', 'q3'},
    {'a', 'b'},
    {
      ('q1', 'b'): {'q2'},
      ('q1', ''): {'q3'},
      ('q2', 'a'): {'q2', 'q3'},
      ('q2', 'b'): {'q3'},
      ('q3', 'a'): {'q1'}
    },
    'q1',
    {'q1'}
    )

assert nfa_1_35.accept('')
assert nfa_1_35.accept('a')
assert nfa_1_35.accept('baba')
assert nfa_1_35.accept('baa')
assert not nfa_1_35.accept('b')
assert not nfa_1_35.accept('bb')
assert not nfa_1_35.accept('babba')
