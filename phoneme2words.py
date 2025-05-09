
from typing import List, Dict
import numpy as np

class wordphoneme:
    def __init__(self, word = None, phoneme = None):
        self._word = ""
        self.word = word

        self._phoneme = ""
        self.phoneme = phoneme

    @property
    def word(self):
        return self._word
    @word.setter
    def word(self, value):
        if len(value) == 0:
            raise ValueError("Attempted empty word..")
        self._word = value

    @property
    def phoneme(self):
        return self._phoneme

    @phoneme.setter
    def phoneme(self, value):
        if len(value) == 0:
            raise ValueError("Attempted empty phoneme..")
        self._phoneme = value

    def __hash__(self):
        return hash(self.word) + hash(self.phoneme)

class WordsPhoneme:

    def __init__(self):
        self._word_phoneme_dictionary: Dict = {}

    @property
    def word_phoneme_dictionary(self):
        return self._word_phoneme_dictionary

    @word_phoneme_dictionary.setter
    def word_phoneme_dictionary(self, wp_obj: wordphoneme):
        assert isinstance(wp_obj, wordphoneme)

        if(wp_obj not in self._word_phoneme_dictionary):
            # A sample way of storing word->phenom. It might not be most efficient way, but considered the repetitive feature of the words as well as the phenoms.
            self._word_phoneme_dictionary.update({wp_obj: [wp_obj.word, wp_obj.phoneme]})


    def put_word_phenom(self, word = None, phoneme = None):
        wp_obj = wordphoneme(word=word, phoneme=phoneme)
        self.word_phoneme_dictionary = wp_obj


class WordPhenomActiveSearch:
    def __init__(self, words_phenom_obj: WordsPhoneme):
        assert isinstance(words_phenom_obj, WordsPhoneme)
        self.words_phenom_obj = words_phenom_obj
        self.searched_phenom_tokens_list: List = []
        self.token_index = 0
        self.currently_matched: Dict = self.words_phenom_obj.word_phoneme_dictionary

    def search_by_phenom_token(self, phoneme_token:str):
        self.searched_phenom_tokens_list += [phoneme_token]
        print(f"searching {' '.join(self.searched_phenom_tokens_list)} on currently matched: {self.currently_matched}")
        currently_matched = {}
        complete_match = {}
        for wp_obj, [word, phenom] in self.currently_matched.items():
            if(' '.join(self.searched_phenom_tokens_list) == phenom):
                complete_match.update({wp_obj: [word, phenom]})
            elif(' '.join(self.searched_phenom_tokens_list) in phenom):
                currently_matched.update({wp_obj: [word, phenom]})

        self.currently_matched = currently_matched

        if(complete_match):
            return 2, complete_match  # match found, but maybe you find more later
        if(not self.currently_matched):
            return 0, None  # no match found

        return 1, None # might the match happens later

    def __del__(self):
        del self.words_phenom_obj
        del self.searched_phenom_tokens_list
        del self.token_index
        del self.currently_matched



#

def invest_core(phonemes: List[str], recognized_words: List, active_search_obj: WordPhenomActiveSearch, words_phenom_obj: WordsPhoneme):
    """
    It's a recursive function.

    """
    if len(phonemes) == 0:
        assert isinstance(recognized_words, list), f"type of recognized_words_ is not list: {type(recognized_words)}"
        return 1, recognized_words

    status, result = active_search_obj.search_by_phenom_token(phonemes[0])

    all_possible_words = []
    if(status == 2): # a word or several words recognized

        for word_phenom_obj, [word, phenom] in result.items():
            # new active_search_obj required ..
            active_search_obj_ = WordPhenomActiveSearch(words_phenom_obj)
            sign, recognized_words_ = invest_core(phonemes[1:], recognized_words + [word], active_search_obj_, words_phenom_obj)
            assert isinstance(recognized_words_, list), f"type of recognized_words_ is not list: {type(recognized_words_)}"

            if(sign == 1): # end up with
                # print(f"+++ all_possible_words: {all_possible_words}, recognized_words_: {recognized_words_}")
                if(len(recognized_words_) > 0 and isinstance(recognized_words_[0],list)): # recognized_word_ itself is in all_possible format, i.e. [[], []].

                    all_possible_words += recognized_words_
                elif(len(recognized_words_) > 0):
                    all_possible_words.append(recognized_words_)
            else: # no word recognized
                pass



    elif(status == 0): # no match found
        return 0, []



    if(status == 1):
        if(len(phonemes) == 1):
            # This capture the cases that the last phenom met but no complete match found ..
            return 0, []
        else: # status being 1, i.e. there is a match in the word-phonem dict but there has not been complete match
            # let investigate further in the case of status == 1 or just for curiosity after match found
            sign, recognized_words_2 = invest_core(phonemes[1:], recognized_words, active_search_obj, words_phenom_obj)

    # sign, recognized_words_2 = invest_core(phonemes, recognized_words, active_search_obj, words_phenom_obj)

            # assert isinstance(recognized_words_, list), f"type of recognized_words_ is not list: {type(recognized_words_)}"
            if (sign == 1):  # end up with
                # print(f"**** all_possible_words: {all_possible_words}, recognized_words_: {recognized_words_2}")
                if (len(recognized_words_2) > 0 and isinstance(recognized_words_2[0],list)):  # recognized_word_ itself is in all_possible format, i.e. [[], []].
                    all_possible_words += recognized_words_2
                elif(len(recognized_words_2) > 0):
                    all_possible_words.append(recognized_words_2)



    if (len(all_possible_words) == 1 and isinstance(all_possible_words[0], list)):  # to prevent excessive []
        all_possible_words = all_possible_words[0]
    if (len(all_possible_words) == 0):
        return 0, []
    else:
        return 1, all_possible_words



def find_word_combos_with_pronunciation(phonemes: List[str], words_phenom_obj: WordsPhoneme) -> List[List[str]]:
    recognized_words = []
    active_search_obj =  WordPhenomActiveSearch(words_phenom_obj)
    sign, all_possible_words = invest_core(phonemes, recognized_words, active_search_obj, words_phenom_obj)

    print(f"sign: {sign} ; all_possible_words: {all_possible_words}")




WORD_PHONEME_LIST = [
    ["ABACUS", "AE B AH K AH S"],
    ["BOOK", "B UH K"],
    ["THEIR", "DH EH R"],
    ["THERE", "DH EH R"],
    ["TOMATO", "T AH M AA T OW"],
    ["TOMATO", "T AH M EY T OW"]
]

if __name__ == "__main__":
    # create word-phenom data
    words_phenom_obj = WordsPhoneme()
    for [word, phenom] in WORD_PHONEME_LIST:
        words_phenom_obj.put_word_phenom(word= word, phoneme= phenom)


    # create sample phonem list
    sample_phoneme_list = ["DH", "EH", "R", "DH", "EH", "R"]
    # create active search capability of 'words_phenom_obj'
    find_word_combos_with_pronunciation(sample_phoneme_list, words_phenom_obj)