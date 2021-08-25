'''
To run the unittests for this module execute the following
python -m unittest discover -p "<path_to_this_file>"
'''

import unittest

#This is a decorating method for enforcing args are of type string
#Tested implicitly by the test_validity_check unittests
def ensure_str():
    def wrapper(f):
        def check(*args):
            #If every arg is a string run the decorated function
            if all([isinstance(arg, str) for arg in args]):
                return f(*args)
            #Otherwise, return false, 'sentence' is not of type string and cannot be valid
            return False
        return check
    return wrapper

def _start_capital(sentence):
    '''
    Returns true if the sentence provided as argument starts with a capital letter
    sentence: (str) -- The sentence to check
    '''
    if not sentence[0].isupper():
        return False
    return True

def _even_quotes(sentence):
    '''
    Returns true if the sentence provided as argument has an even number of double-quote marks
    sentence: (str) -- The sentence to check
    '''
    if sentence.count('"') % 2 is not 0:
        return False
    return True

def _one_period(sentence):
    '''
    Returns true if the sentence provided as argument contains only 1 period
    sentence: (str) -- The sentence to check
    '''
    if sentence.count(".") != 1:
        return False
    return True

def _end_period(sentence):
    '''
    Returns true if the sentence provided as argument ends with a period
    sentence: (str) -- The sentence to check
    '''
    if sentence[-1] != ".":
        return False
    return True

def _spell_numbers(sentence):
    '''
    Returns true so long as the numbers in the sentence provided that are less than 13
    are spelt out rather than in their numerical form
    *NOTE* - It does not ensure that numbers 13 and above are always in numerical form
    sentence: (str) -- The sentence to check
    '''
    for word in sentence.split(" "):
        try:
            cast = int(word)
            if cast < 13:
                return False
        except ValueError:
            continue
    return True

@ensure_str()
def validity_check(sentence):
    '''
    Returns true if the sentence matches the rules required to designate a valid sentence
    Decorator ensures that sentence arg is of type str
    sentence: (str) - The string to check for validity with ruleset
    '''
    # Rule 1
    if not _start_capital(sentence):
        return False
    # Rule 2
    if not _even_quotes(sentence):
        return False
    # Rule 4 precludes Rule 3
    if not _one_period(sentence):
        return False
    # Rule 3
    if not _end_period(sentence):
        return False
    # Rule 5
    if not _spell_numbers(sentence):
        return False
    return True

#Unit tests
class validity_check_tests(unittest.TestCase):
    '''
    Unit test class for validity functions and the overall validity check itself
    '''
    valid_sentences = ['The quick brown fox said "hello Mr lazy dog".',
                       'The quick brown fox said hello Mr lazy dog.',
                       'One lazy dog is too few, 13 is too many.',
                       'One lazy dog is too few, thirteen is too many.']

    invalid_sentences = ['The quick brown fox said "hello Mr. lazy dog".',
                         'the quick brown fox said "hello Mr lazy dog".',
                         'The quick brown fox said "hello Mr lazy dog."',
                         'One lazy dog is too few, 12 is too many.']

    # Check non str are not allowed
    # List contains: int, float, long, complex, list, dict, tuple, set, bool
    excluded_types = [5, 5.0, 5L, 5J, ["xyz"], {"xyz": 123}, ("abc", 123), set([1, 1, 2, 3]), False]

    def test_start_capital(self):
        '''
        Test the start_capital function
        Checks that sentences start with a capital letter
        '''
        self.assertTrue(_start_capital("Hello world"))
        self.assertFalse(_start_capital("hello world"))
        self.assertFalse(_start_capital("23"))

    def test_even_quotes(self):
        '''
        Test the even_quotes function
        Checks that sentences contain an even number of double quotes
        '''
        self.assertTrue(_even_quotes('""'))
        self.assertFalse(_even_quotes('"'))
        self.assertTrue(_even_quotes('""""'))
        self.assertFalse(_even_quotes('"""'))

    def test_one_period(self):
        '''
        Test the one_period function
        Checks that sentences can only contain 1 period
        '''
        self.assertTrue(_one_period("Hello."))
        self.assertFalse(_one_period(".Hello."))
        self.assertFalse(_one_period("hello"))

    def test_end_period(self):
        '''
        Test the end_period function
        Checks that sentences must end with a period
        '''
        self.assertTrue(_end_period("Hello."))
        self.assertTrue(_end_period(".Hello."))
        self.assertFalse(_end_period(".Hello"))

    def test_spell_numbers(self):
        '''
        Test the spell_numbers function
        Checks that numbers below 13 are spelt
        Checks that 13 can be spelt or numericised
        '''
        self.assertTrue(_spell_numbers("twelve"))
        self.assertFalse(_spell_numbers("12"))
        self.assertTrue(_spell_numbers("13"))
        self.assertTrue(_spell_numbers("Thirteen"))
        self.assertTrue(_spell_numbers("20"))
        self.assertTrue(_spell_numbers("twenty"))
        self.assertFalse(_spell_numbers("0"))
        self.assertTrue(_spell_numbers("zero"))

    def test_validity_check(self):
        '''
        Test the validity checker function
        Checks valid sentences, invalid sentences and finally invalid types
        '''
        for sen in self.valid_sentences:
            self.assertTrue(validity_check(sen))

        for sen in self.invalid_sentences:
            self.assertFalse(validity_check(sen))

        #Check types, only string allowed, all others are excluded
        for typ in self.excluded_types:
            self.assertFalse(validity_check(typ))
