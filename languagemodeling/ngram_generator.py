from collections import defaultdict
import random


class NGramGenerator(object):

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self._n = model._n
        
        # compute the probabilities
        probs = defaultdict(dict)
        for ngram, count in model._count.items():
            probs[ngram[:-1]][ngram[-1]] = count / model._count_menos[ngram[:-1]]
        self._probs = probs
        # sort in descending order for efficient sampling
        my_sorted = lambda xs: sorted(xs, key=lambda x: (-x[1], x[0]))
        self._sorted_probs = sorted_probs = {}
        for prev_tokens, prob_dict in probs.items():
            sorted_probs[prev_tokens] = my_sorted(prob_dict.items())
       
        print(my_sorted)

    def generate_sent(self):
        """Randomly generate a sentence."""
        n = self._n
        sent = []
        prev_tokens = ('<s>',) * (n - 1)
        token = '<s>'
        while token != '</s>':
            token = self.generate_token(tuple(prev_tokens))
            #problist = tuple(prev_tokens) #list(self._probs[token].items())
            sent.append(token)
            prev_tokens = (prev_tokens+(token,))[1:]            

        return sent[:-1]

    def generate_token(self, prev_tokens):#=None):
        """Randomly generate a token, given prev_tokens.

        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self._n
        if not prev_tokens:
            prev_tokens = ()
        assert len(prev_tokens) == n - 1

        r = random.random()
        i = 0
        probs = self._sorted_probs[prev_tokens]
        token, prob = probs[0]
        acum = prob

        while r > acum:
            i += 1
            token, prob = probs[i]
            acum += prob

        return token

       