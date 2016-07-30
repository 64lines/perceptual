#!/usr/bin/python
from utils import get_file_lines

messages = {
    'lang': 'What is the language you want to work with? (en/es): ',
    'word': 'Please include a polarity and a word in this format: "p - word"\n',
    'saved': 'The word has been saved in'
}

polarities = {
    'p': 'positive',
    'n': 'negative'
}

def get_element(text, pos):
    return text.split(" - ")[pos].lower()

def message(id):
    return messages[id]

def build_path(lang, polarity):
    return "inputs/%s_words_%s.txt" % (polarities[polarity], lang)

def text_format(text):
    return "\n%s" % text

def save_word(word, path):
    if word not in get_file_lines(path):
        with open(path, "a") as polarity_file:
            polarity_file.write(text_format(word))
            return "%s %s" % (message('saved'), path)
    return ""

def manual_classifier(lang, text):
    return save_word(get_element(text, 1), build_path(lang, get_element(text, 0)))

print manual_classifier(raw_input(message('lang')), raw_input(message('word')))