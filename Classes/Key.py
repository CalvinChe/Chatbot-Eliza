import re


class Key():
    '''
    A Class to represent a weighted Key
    ...

    Attributes
    ----------
    word : str
        the corresponding word the key represents.
    weight : int
        the weight of the key, the larger the weight the more important the word
    decomps : Decomposition
        list of total decompositions which correspond to the key

    Methods
    -------
    matchWord():
        check if the input matches the key returns a regex Match Obj if found None otherwise
    cmp(key2):
        compares the key to another key to it's weight
    addDecomp(decomp):
        adds a new decomposition to the list of decompositions
    matchDecomp(match):
        matches str to a corresponding decomposition and returns a formated reply

    '''

    def __init__(self, word, weight, *decomps):
        '''
        Constructor of the Key class

        parameters
        ----------
        word : str
            corresponding word of the key
        weight : int
            the weight of the key, the larger the wieght the more important the word
        *decomps : Decompositions
            variable amount of Decompositions to insert into self.decomps
        '''
        self.word = word
        self.weight = weight
        self.decomps = []
        for decomp in decomps:
            self.addDecomp(decomp)

    def matchWord(self, input):
        '''
        check if the input matches the key returns a regex Match Obj if found None otherwise

        parameters
        ---------
        input : str
            the user input

        return
        ------
        regex Match Object if found
        None

        '''
        if re.search(r"\b" + self.word, input, re.IGNORECASE):
            return self
        return None

    def cmp(self, key2):
        '''
        compares the current key to another key

        parameters
        ---------
        key2 : Key
            other key

        return
        ------
        returns 0 if weights are the same
        returns -1 if current key's weight < key2's weight
        returns 1 if current key's weight > key2's weight

        '''
        if self.weight == key2.weight:
            return 0
        elif self.weight < key2.weight:
            return -1
        else:
            return 1

    def addDecomp(self, decomp):
        '''
        Adds new Decomposition object to list of decompositions

        parameters
        ---------
        decomps : Decomposition
            a decomposition to add to self.Decomps

        returns
        ------
        None

        '''
        self.decomps.append(decomp)

    def matchDecomp(self, input):
        '''
        Matches corresponding Decompositions with Input to have a less generic response

        parameters
        ---------
        input : str
            the user input

        returns
        -------
        corresponding decomposition patterns if matched
        None

        '''
        for decomp in self.decomps:
            match = re.match(decomp.structure, input, re.IGNORECASE)
            if match:
                return decomp.selectPattern(match)

        return None
