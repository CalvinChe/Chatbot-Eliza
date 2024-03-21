from Classes.Synonym import Synonym
from Classes.Key import Key
from Classes.Decomposition import Decomposition
import json
import re


class Eliza:
    '''
    A psychiatric chatbot with Python based on Weizenbuam's ELIZA
    ...

    Attributes
    ----------
    keys : Key
        list of weighted Key obj which we search
    synonymsPre : Synonym
        list of words we use to clean up a user's input before matching
    synonymsPost : Synonym
        list of words we replace when replacing a user's input

    Methods
    -------
    loadKeys():
        loads list of keys from json file.
    loadSynonyms():
        load pre and post synonyms from json file.
    respond():
        given a user's input, return a corresponding output
    cleanInput():
        prepares input to be matched and responded with.
    chat():
        main loop to chat with user.

    '''

    def __init__(self):
        '''
        Constructor for the Eliza Class
        '''
        self.keys = []
        self.synonymsPost = []
        self.synonymsPre = []
        self.input = ""
        self.loadSynonyms()
        self.loadKeys()

    def loadKeys(self):
        '''
        load keys from json file and store it inside self.keys

        Parameters
        ---------
        None

        Return
        ------
        None
        '''
        # Load keys from json file.
        with open("./Data/keys.json", "r") as file:
            data = json.load(file)
        for key in data:
            decomps = []
            for decomp in key["decomps"]:
                decomps.append(Decomposition(
                    decomp["structure"], self.synonymsPost, *decomp["pattern"]))
            self.keys.append(Key(key["word"], key["weight"], *decomps))

    def loadSynonyms(self):
        '''
        load and store synonyms from json file for post and pre replacement

        Parameters
        ---------
        None

        Return
        ------
        None
        '''
        # Load data from json for synonymsPost and synonymsPre
        with open("./Data/synonymsPost.json", "r") as file:
            data = json.load(file)
        for syn in data:
            self.synonymsPost.append(Synonym(syn["word"], syn["subs"]))

        with open("./Data/synonymsPre.json", "r") as file:
            data = json.load(file)
        for syn in data:
            self.synonymsPre.append(Synonym(syn["word"], syn["subs"]))

    def respond(self):
        '''
        Responds to user input by
        1. cleans user input
        2. check for keyword and choose the highest weighted one
        3. If no keyword is matched, reply with a generic response.
        4. utilize keyword to return matching reply and return it.

        Parameters
        ---------
        None

        Return
        ------
        response : str
        '''
        self.cleanInput()
        pKey = self.keys[0]
        for key in self.keys:
            localMatch = key.matchWord(self.input)
            if localMatch and pKey.cmp(localMatch) <= 0:
                pKey = localMatch

        output = pKey.matchDecomp(self.input)
        if not output:
            return self.keys[0].matchDecomp("")
        return output

    def cleanInput(self):
        '''
        cleans user input to prepare it for matching
        cleans input by stopping input at first punctuation
        substitutes similar words to one specific word to maximize matches

        Parameters
        ---------
        None

        Return
        ------
        None
        '''
        punctuation_index = next(
            (i for i, char in enumerate(self.input) if char in ".!?"), None)
        self.input = self.input[:punctuation_index]

        # replace input with corresponding synonyms
        for synonym in self.synonymsPre:
            pattern = rf"\b{ '|'.join(synonym.subs)}\b"
            self.input = re.sub(pattern, synonym.word,
                                self.input, flags=re.IGNORECASE)

    def chat(self):
        '''
        initiate chat with the bot.
        the bot will prompt an input and respond to the user
        until goodbye is typed.

        Parameters
        ---------
        None

        Return
        ------
        None
        '''
        print("HOW DO YOU DO. PLEASE TELL ME YOUR PROBLEM")
        while True:
            self.input = input("input: ")
            if str.lower(self.input) == 'goodbye':
                break
            print(self.respond())


def main():
    eliza = Eliza()
    eliza.chat()


if __name__ == "__main__":
    main()
