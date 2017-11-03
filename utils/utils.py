#!/usr/bin/python
# -*- coding: latin-1 -*-

class Formatter():
    def format_text(self, text):
        chars_to_replace = [
            '#', '?', '!', '.', '\"', ',', '\'', '�',
            ')', '(', '¡', '¿']
        text = text.strip().lower()

        # Removing literal marks.
        for char in chars_to_replace:
            text = text.replace(char, '')
        
        text = text.replace('.', '. ') \
            .replace(',', ', ') \
            .replace('  ', ' ') \

        text = self.remove_links(text)
        text = self.remove_mentions(text)

        return text
    
    def remove_links(self, text):
        list_words = text.split(' ')
        result_list = []
        for word in list_words:
            if not '://' in word:
                result_list.append(word)

        return ' '.join(result_list)

    def remove_mentions(self, text):
        list_words = text.split(' ')
        result_list = []
        for word in list_words:
            if not '@' in word:
                result_list.append(word)

        return ' '.join(result_list)