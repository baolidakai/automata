from utils import *
# Tests for the utils

dfa_1_9 = DFA(
    {'q1', 'q2'},
    {'0', '1'},
    {('q1', '0'): 'q1',
     ('q1', '1'): 'q2',
     ('q2', '0'): 'q1',
     ('q2', '1'): 'q2'},
    'q1',
    {'q1'}
    )
nfa_1_9 = DFA2NFA(dfa_1_9)
assert nfa_1_9.accept('')
assert nfa_1_9.accept('0')
assert not nfa_1_9.accept('1')
assert not nfa_1_9.accept('001')
assert nfa_1_9.accept('0010')

# Figure 1.22 in Siepser's
dfa_1_22 = DFA(
    {'q', 'q0', 'q00', 'q001'},
    {'0', '1'},
    {('q', '0'): 'q0',
     ('q', '1'): 'q',
     ('q0', '0'): 'q00',
     ('q0', '1'): 'q',
     ('q00', '0'): 'q00',
     ('q00', '1'): 'q001',
     ('q001', '0'): 'q001',
     ('q001', '1'): 'q001'
    },
    'q',
    {'q001'}
    )
nfa_1_22 = DFA2NFA(dfa_1_22)
# nfa_1_22 should accept w if and only if w contains 001
assert nfa_1_22.accept('001')
assert nfa_1_22.accept('1001')
assert nfa_1_22.accept('11001')
assert nfa_1_22.accept('00100')
assert not nfa_1_22.accept('')
assert not nfa_1_22.accept('000')
assert not nfa_1_22.accept('01010')
