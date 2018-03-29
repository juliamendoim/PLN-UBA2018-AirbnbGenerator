# https://docs.python.org/3/library/collections.html
from collections import defaultdict
import math


class LanguageModel(object):

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        return 0.0

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        return -math.inf

    def log_prob(self, sents):
        result = 0.0
        for i, sent in enumerate(sents):
            lp = self.sent_log_prob(sent)
            if lp == -math.inf:
                return lp
            result += lp
        return result

    def cross_entropy(self, sents):
        log_prob = self.log_prob(sents)
        n = sum(len(sent) + 1 for sent in sents)  # count '</s>' events
        e = - log_prob / n
        return e

    def perplexity(self, sents):
        return math.pow(2.0, self.cross_entropy(sents))


class NGram(LanguageModel):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self._n = n

        count = defaultdict(int)
        count_menos = defaultdict(int)

        m = n-1 

        
        #import pdb; pdb.set_trace()

        for sent in sents:
            
            sent = ['<s>'] * (n-1) + sent + ['</s>']

            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i:i+n])  # los diccionarios no pueden guardar listas, pero sí tuplas
                count[ngram] += 1
          
            for i in range(len(sent) - m):
                ngram = tuple(sent[i:i+m])  # los diccionarios no pueden guardar listas, pero sí tuplas
                count_menos[ngram] += 1


        self._count_menos = dict(count_menos)
        self._count = dict(count)

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        if len(tokens) == self._n:
            return self._count.get(tokens, 0)
        else:
            return self._count_menos.get(tokens, 0)

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        if prev_tokens == None:
            prev_tokens = ()
        # WORK HERE!!
        tokens = prev_tokens + (token,)
        # if self._count_menos.get(prev_tokens, 0) != 0:
        return self._count.get(tokens, 0) / self._count_menos.get(prev_tokens, 0)
        # else:
        #     return 0.0


    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        # WORK HERE!!

        n = self._n

        prev_tokens = ('<s>',)*(n-1)
        producto = 1
        for token in sent+['</s>']:
            prob_ngrams = self.cond_prob(token, prev_tokens)
            if prob_ngrams == 0.0:
                return 0.0
            producto = producto * prob_ngrams
            prev_tokens = (prev_tokens+(token,))[1:]
        
        return producto
        
        
    def sent_log_prob(self, sent):


        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        # WORK HERE!!


        n = self._n

        prev_tokens = ('<s>',)*(n-1)
        suma = 0.0
        for token in sent+['</s>']:
            prob_ngrams = self.cond_prob(token, prev_tokens)
            if prob_ngrams != 0.0:
                log_ngrams = math.log(prob_ngrams,2)
                suma = suma + log_ngrams
                prev_tokens = (prev_tokens+(token,))[1:]
            else:
                return -math.inf

        return suma


