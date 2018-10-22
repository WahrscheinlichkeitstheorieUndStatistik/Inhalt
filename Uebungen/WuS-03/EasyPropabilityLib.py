# coding: utf-8

# <div class="alert alert-block alert-info">
# <h1> A small library for simple discrete Probability tasks like card games, urns etc.</h1>
# <h2> classes: ProbDist(dict), Dist(Counter)</h2>
# <h2> functions: P(event,space), such_that, cross, choose, ball, combos, such_that,  joint</h2>
# </div>

# In[120]:


import itertools #for combos
from fractions import Fraction #for results of P
from math import factorial #for choose
import random #to sample randomly
from collections import Counter # for Dist class


# # class: ProbDistribution 
# ## a dictionary, which maps {outcomes: probability}, normalies

# In[121]:


class ProbDist(dict):
    "A Probability Distribution; an {outcome: probability} mapping."
    def __init__(self, mapping=(), **kwargs):
        self.update(mapping, **kwargs)
        # Make probabilities sum to 1.0; assert no negative probabilities
        total = sum(self.values())
        for outcome in self:
            self[outcome] = self[outcome] / total
            assert self[outcome] >= 0
            


# In[122]:


#test case
#Dr Gelb and Dr Blau from simpson paradox
# S == success F == fail H == heart B == band aid

#DrGelb = ProbDist(SH=70, FH=20, SB=10, FB=0)
#DrBlau = ProbDist(SH= 2, FH= 8, SB=81, FB=9)
#print(DrGelb)
#print(DrBlau)


# ## use case: Simpsons Paradox

# In[123]:


#compare heart ops
#print(DrGelb['SH']/(DrGelb['SH']+DrGelb['FH']) > DrBlau['SH']/(DrBlau['SH']+DrBlau['FH']))
#compare band-aid ops
#print(DrGelb['SB']/(DrGelb['SB']+DrGelb['FB']) > DrBlau['SB']/(DrBlau['SB']+DrBlau['FB']))
#print('Dr Gelb is more successful if both parts are taken seperately')


# In[124]:


#compare all ops
#print((DrGelb['SH']+DrGelb['SB']) > (DrBlau['SH']+DrBlau['SB']))
#print('yet if we take Total Propabilies NOT so !')


# # class: Distribution
# ## similar to ProbDist yet NO normalization AND very versatile constructor

# In[125]:


class Dist(Counter): 
    "A Distribution of {outcome: frequency} pairs."


# In[126]:


#test cases: 
## A set of equiprobable outcomes:
#Dist({1, 2, 3, 4, 5, 6})


# In[127]:


#test cases: 
##A collection of outcomes, with repetition indicating frequency:
#Dist('THHHTTHHT')


# In[128]:


#test cases: 
## A set of equiprobable outcomes:
#Dist({1, 2, 3, 4, 5, 6})


# In[129]:


#test cases: 
## A mapping of {outcome: frequency} pairs:
#Dist({'H': 5, 'T': 4})


# In[130]:


#test cases: 
## Keyword arguments:
#Dist(H=5, T=4) == Dist({'H': 5}, T=4) == Dist('TTTT', H=5)


# # function: P(event,space)

# In[131]:


def P(event, space): 
    """The probability of an event, given a sample space of equiprobable outcomes. 
    event: a collection of outcomes, or a predicate that is true of outcomes in the event. 
    space: a set of outcomes or a probability distribution of {outcome: frequency}."""
    if callable(event):
        event = such_that(event, space)
    if isinstance(space, ProbDist):
        return sum(space[o] for o in space if o in event)
    else:
        return Fraction(len(event & space), len(space))


# In[132]:


#test case for P(event,space)
#D     = {1, 2, 3, 4, 5, 6} # a sample space
#even  = {   2,    4,    6} # an event

#P(even, D)


# # such_that : outcomes in the sample space for which the predicate is true

# In[133]:


def such_that(predicate, space): 
    """The outcomes in the sample space for which the predicate is true.
    If space is a set, return a subset {outcome,...};
    if space is a ProbDist, return a ProbDist {outcome: frequency,...};
    in both cases only with outcomes where predicate(element) is true."""
    if isinstance(space, ProbDist):
        return ProbDist({o:space[o] for o in space if predicate(o)})
    else:
        return {o for o in space if predicate(o)}


# In[134]:


#test case, "B"oys and "G"irls, first letter is OLDER
#e.g. 'BG' to denote the outcome in which the older child is a boy and the younger a girl.

#S = {'BG', 'BB', 'GB', 'GG'}


# In[135]:


#def two_boys(outcome): return outcome.count('B') == 2

#def older_is_a_boy(outcome): return outcome.startswith('B')

#P(two_boys, such_that(older_is_a_boy, S))


# In[136]:


#def at_least_one_boy(outcome): return 'B' in outcome

#P(two_boys, such_that(at_least_one_boy, S))


# In[137]:


#such_that(at_least_one_boy, S)


# # cross fct (cartesian product)

# In[138]:


def cross(A, B):
    "The set of ways of concatenating one item from collection A with one from B."
    return {a + b 
            for a in A for b in B}


# In[139]:


#test case for "cross"
#suits = u'♥♠♦♣'
#ranks = u'AKQJT98765432'

#myDeck = cross(suits,ranks)
#print(myDeck)


# In[140]:


#test case for "cross": find all cross
#mycross = {s for s in myDeck if s[0]==u'♣'}
#len(mycross)


# In[141]:


#test case for "cross"
#bgbirthdays = cross('BG', '1234567')
#print(bgbirthdays)


# In[142]:


#test case for "cross"
#S3 = cross(bgbirthdays, bgbirthdays);len(S3)


# # choose fct (binomial coefficient)

# In[92]:


def choose(n, c):
    "Number of ways to choose c items from a list of n items."
    return factorial(n) // (factorial(n - c) * factorial(c))


# In[93]:


#choose(9, 6)


# # fill an urn : many balls 

# In[94]:


def balls(color, n):
    "A set of n numbered balls of the given color."
    return {color + str(i)
            for i in range(1, n + 1)}


# In[95]:


#test case
#urn = balls('B', 6) | balls('R', 9) | balls('W', 8)
#print(len(urn))
#random.sample(urn,7)


# # combos => fully generate all combinations

# In[96]:


def combos(items, n):
    "All combinations of n items; each combo as a space-separated str."
    return set(map(' '.join, itertools.combinations(items, n)))


# In[97]:


#test case
#Hands = combos(myDeck, 5)
#print(len(Hands))
#random.sample(Hands,7)


# In[99]:


#test case
#flush = {hand for hand in Hands if any(hand.count(suit) == 5 for suit in suits)}
#P(flush, Hands)


# In[100]:


#four_kind = {hand for hand in Hands if any(hand.count(rank) == 4 for rank in ranks)}

#P(four_kind, Hands)


# ## use case: hands which contain 3 aces

# In[146]:


#def _3aces(sample): return sample.count('A') == 3


# In[147]:


#P(_3aces, Hands)


# In[158]:


#test case 1
#Hands = combos(myDeck, 6)
#exact = P(_3aces, Hands)
#print(exact)


# In[149]:


#_3acesin4 = choose(4,3);print(_3acesin4)


# In[152]:


#_3nonacesin48 = choose(48,3);print(_3nonacesin48)


# In[171]:


#test case 2
#U6 = combos(urn, 6)
#random.sample(U6, 5)


# ## function: select n balls of a given color in an urn

# In[178]:


def select(color, n, space):
    "The subset of the sample space with exactly `n` balls of given `color`."
    return {s for s in space if s.count(color) == n}


# In[180]:


#test case
#U6 = combos(urn, 6)
#N = len(U6)

#assert N * P(select('R', 6), U6) == choose(9, 6)


# In[174]:


#N * P(select('B', 3) & select('W', 2) & select('R', 1), U6) == choose(6, 3) * choose(8, 2) * choose(9, 1)


# In[175]:


#N * P(select('W', 4), U6) == choose(8, 4) * choose(6 + 9, 2)  # (6 + 9 non-white balls)


# In[176]:


#P(select('W', 3), U6)


# ## function: joint gives the distribution of two independent distributions.

# In[182]:


def joint(A, B, combine='{}{}'.format):
    """The joint distribution of two independent distributions. 
    Result is all entries of the form {'ab': frequency(a) * frequency(b)}"""
    return Dist({combine(a, b): A[a] * B[b]
                 for a in A for b in B})


# In[185]:


#test case
#die6 = Dist({6: 1/6, '-': 5/6})

#two6s = joint(die6, die6)
#two6s


# In[186]:


#bernoulli chain, length 2, p = 1/6

