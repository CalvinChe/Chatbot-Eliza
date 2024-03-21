class Synonym():
    '''
    A class that represents a synonym where we have
    one word that can represent multiple words

    Attributes
    ---------
    word : str
        Main word that represents multiple other words
    subs : str []
        list of words to get replaced with main word

    Methods
    -------
    apply(sub):
        given a sub, return the word if sub is in self.subs
    '''

    def __init__(self, word, matches):
        '''
        Constructor class for Synonym Class

        parameters
        ---------
        word : str
            Main word that represents multiple other words
        mathes : str []
            list of strings which are synonyms with the main word
        '''
        self.word = word
        self.subs = []
        for m in matches:
            self.subs.append(m)

    def apply(self, sub):
        '''
        Helper class which returns the main word if sub is in self.subs

        parameters
        ----------
        sub : str
            The word we try to substitute

        return
        ---------
        self.word --if sub is in self.subs
        sub      -- if sub not in self.subs
        '''
        if sub in self.subs:
            return self.word
        return sub
