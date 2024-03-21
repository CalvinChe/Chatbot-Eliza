import re


class Decomposition():
    '''
    A class to represent possible Decompositions of a Key
    ...

    Attributes
    ---------
    synonymsPost : Synonyms
        list of synonyms to substitute input after matching
    structure : str
        a regex string to match input to the input
    pattern : str
        list of unformatted strings to match to decompositions
    index : int
        current index of specific patterns

    '''

    def __init__(self, structure, synonymsPost, *patterns):
        '''
        Constructor for Decompostion class

        parameters
        ---------
        structure : str
            structure of the regex expression used to match decompostion.
        synonymsPost : Synonyms
            list of synonyms to substitute input after matching
        patterns : Str
            List of unformatted strings to match with decompositions
        '''
        self.synonymsPost = synonymsPost
        self.structure = structure
        self.pattern = []
        self.index = 0
        for pattern in patterns:
            self.addPattern(pattern)

    def addPattern(self, pattern):
        '''
        Helper class to add patterns to list of patterns

        Parameters
        ---------
        pattern : str
            an unformmated string

        Returns
        --------
        None
        '''
        self.pattern.append(pattern)

    def selectPattern(self, match):
        '''
        Selects a Pattern and format the string before returning it.

        Parameters
        ---------
        match : RE.Match Obj
            the regex match object that corresponds to our input

        Returns
        -------
        str : formatted String reply
        '''
        curr = self.index
        self.index += 1
        if self.index == len(self.pattern):
            self.index = 0

        groups = [*match.groups()]
        for i, group in enumerate(groups):
            if group:
                transformed = self.cleanOutput(group)
                groups[i] = transformed
        return self.pattern[curr].format(*groups)

    def cleanOutput(self, input):
        '''
        Replace input words with corresponding Synonyms

        Parameters
        ----------
        input : str
            input string of user

        Return
        ------
        str : substituted input
        '''
        for synonym in self.synonymsPost:
            pattern = rf"\b{ '|'.join(synonym.subs)}\b"
            input = re.sub(pattern, synonym.word, input, flags=re.IGNORECASE)
        return input
