
Phoneme2Word
Given a sequence of phonemes as input, **WordsPhoneme** finds all the combinations of the words that can produce this sequence.



A phoneme is a sound unit (similar to a character for text). We have an extensive pronunciation dictionary (think millions of words). 
Below is a snippet: 
```
ABACUS AE B AH K AH S 
BOOK B UH K 
THEIR DH EH R 
THERE DH EH R 
TOMATO T AH M AA T OW 
TOMATO T AH M EY T OW
```

Given a sequence of phonemes as input (e.g. ["DH", "EH", "R", "DH", "EH", "R"]), find all the combinations of the words that can produce this sequence 
(e.g. [["THEIR", "THEIR"], ["THEIR", "THERE"], [["THERE", "THEIR"], ["THERE", "THERE"]])."


- Word phoneme database should be stored in WORD_PHONEME_LIST like:
``` WORD_PHONEME_LIST = [
    ["ABACUS", "AE B AH K AH S"],
    ["BOOK", "B UH K"],
    ["THEIR", "DH EH R"],
    ["THERE", "DH EH R"],
    ["TOMATO", "T AH M AA T OW"],
    ["TOMATO", "T AH M EY T OW"]
]
```
- The input phoneme is stored in sample_phoneme_list, ex.:
```
sample_phoneme_list = ["DH", "EH", "R", "DH", "EH", "R"]
```
