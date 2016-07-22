#!/usr/bin/python
from utils import get_file_lines

class ManualClassifier:
    def __init__(self):
        self.POSITIVE_TEXT = 'positive'
        self.NEGATIVE_TEXT = 'negative'
        self.language = 'en'
        self.list_positive_words = []
        self.list_negative_words = []

    def add_words(self, positive_words_path, negative_words_path):
        another = True
        while another:
            path = ""
            include_word = True

            separator = " - "
            input = raw_input('Please include a polarity and word (e.g. "p - word"): ')
            polarity = input.split(separator)[0].lower()
            word = input.split(separator)[1].lower()

            if polarity == 'p':
                path = "inputs/%s_words_%s.txt" % (self.language, self.POSITIVE_TEXT)
                self.list_positive_words = get_file_lines(path)

                if word in self.list_positive_words:
                    include_word = False
            elif polarity == 'n':
                path = "inputs/%s_words_%s.txt" % (self.language, self.NEGATIVE_TEXT)
                self.list_negative_words = get_file_lines(path)

                if word in self.list_negative_words:
                    include_word = False

            if include_word:
                print " * Saved in: " % path
                with open(path, "a") as polarity_file:
                    polarity_file.write("\n%s" % word)

            keep_going = raw_input('Do you wanna keep going? (y/n):').lower()

            if keep_going == 'n':
                another = False
            else:
                another = True

    def setup(self):
        lang = raw_input('What is the language you want to work with? (en/es): ')
        self.language = lang.lower()

        if not lang:
            return

        self.add_words(positive_words_path, negative_words_path)

analyzer = ManualClassifier()
analyzer.setup()
