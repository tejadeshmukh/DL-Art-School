""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''

import re
from unidecode import unidecode
from .numbers import normalize_numbers


# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

# # List of (regular expression, replacement) pairs for abbreviations:
# _abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
#   ('mrs', 'misess'),
#   ('mr', 'mister'),
#   ('dr', 'doctor'),
#   ('st', 'saint'),
#   ('co', 'company'),
#   ('jr', 'junior'),
#   ('maj', 'major'),
#   ('gen', 'general'),
#   ('drs', 'doctors'),
#   ('rev', 'reverend'),
#   ('lt', 'lieutenant'),
#   ('hon', 'honorable'),
#   ('sgt', 'sergeant'),
#   ('capt', 'captain'),
#   ('esq', 'esquire'),
#   ('ltd', 'limited'),
#   ('col', 'colonel'),
#   ('ft', 'fort'),
# ]]
_abbreviations = [(re.compile('\\b%s\\.' % x[0]), x[1]) for x in [
  ('डॉ', 'डॉक्टर'),
  ('श्री', 'श्रीमान'),
  ('सुश्री', 'सुश्रीमती'),
  ('प्रो','प्रोफेसर')
  ]
  ]

def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text


def expand_numbers(text):
    # Simple mapping of numbers to their Hindi word equivalents
    num_to_words = {
        '1': 'एक', '2': 'दो', '3': 'तीन', '4': 'चार', '5': 'पांच',
        '6': 'छह', '7': 'सात', '8': 'आठ', '9': 'नौ', '0': 'शून्य'
    }
    # Replace digits with words
    return ''.join(num_to_words.get(char, char) for char in text)


def lowercase(text):
  return text.lower()


def collapse_whitespace(text):
  return re.sub(_whitespace_re, ' ', text)


def convert_to_ascii(text):
  return unidecode(text)


def basic_cleaners(text):
  '''Basic pipeline that lowercases and collapses whitespace without transliteration.'''
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def transliteration_cleaners(text):
  '''Pipeline for non-English text that transliterates to ASCII.'''
  text = normalize_devanagari_characters(text)
  text = expand_abbreviations(text)
  text = collapse_whitespace(text)
  
  return text

# def english_cleaners(text):
#     '''Pipeline for Hindi text, focusing on script normalization and cleanup.'''
#     text = normalize_devanagari_characters(text)
#     text = collapse_whitespace(text)
#     # text = remove_unwanted_characters(text)  # Handles quotes, non-Devanagari characters, etc.
#     return text

def normalize_devanagari_characters(text):
    # Add specific normalization rules here
    return text


# def english_cleaners(text):
#   '''Pipeline for English text, including number and abbreviation expansion.'''
#   text = convert_to_ascii(text)
#   text = lowercase(text)
#   text = expand_numbers(text)
#   text = expand_abbreviations(text)
#   text = collapse_whitespace(text)
#   text = text.replace('"', '')
#   return text
