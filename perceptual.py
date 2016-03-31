# Exec:
# $ python perceptual.py inputs/example_tweets.txt
#!/usr/bin/python
import sys
from utils import get_file_lines

POSITIVE_WORDS_PATH = "inputs/positive_words.txt"
NEGATIVE_WORDS_PATH = "inputs/negative_words.txt"

list_positive_words = get_file_lines(POSITIVE_WORDS_PATH)
list_negative_words = get_file_lines(NEGATIVE_WORDS_PATH)

# Bag of words models using positive, negative and
# neutral statuses.
class BagOfWordsAnalizer():

    def analyze_text(self, text):
        result = ""

        polarities = {
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }

        list_words = text.split(" ")
        for word in list_words:
            word = word.lower()
            if word in list_positive_words:
                polarities["positive"] += 1
            elif word in list_negative_words:
                polarities["negative"] += 1
            else:
                polarities["neutral"] += 1

        if polarities["positive"] > polarities["negative"]:
            result = "positive"
        elif polarities["positive"] < polarities["negative"]:
            result = "negative"
        else:
            result = "neutral"

        return result

# Looks for emoticons to figure out more quickly the
# sentiment of the tweet.
class EmoticonAnalyzer:

    def __init__(self):
        self.dict_emoticon = {
            "positive": [":-P", ";-)", ":-D", ":-)", ":D", ":)", "xD"],
            "negative": [":-||", ":-/", "D-:", ":-(", "D:", ":(", "Dx"]
        }

    def analyze_text(self, text):
        positive_index = 0
        negative_index = 0
        result = ""

        for emoticon in self.dict_emoticon["positive"]:
            if emoticon in text:
                positive_index += 1

        for emoticon in self.dict_emoticon["negative"]:
            if emoticon in text:
                negative_index += 1

        if positive_index > negative_index:
            result = "positive"
        elif negative_index > positive_index:
            result = "negative"
        elif negative_index == positive_index:
            result = "neutral"

        return result

class AnalyzerManager():
    def __init__(self):
        self.result_list = []
        self.bagofwords_analyzer = BagOfWordsAnalizer()
        self.emoticon_analyzer = EmoticonAnalyzer()

    def run_analysis(self, text):
        bagofwords_result = self.bagofwords_analyzer.analyze_text(text)
        emoticons_result = self.emoticon_analyzer.analyze_text(text)

        result = bagofwords_result
        # If there's any positive or negative result in emoticon analyisis
        # so we're taking this one as priority instead others.
        if emoticons_result is not "neutral":
            result = emoticons_result

        self.result_list.append([text, result])

    def get_result_list(self):
        return self.result_list

def main_exec():
    tweets_list = get_file_lines(sys.argv[1])
    manager = AnalyzerManager()

    for tweet in tweets_list:
        manager.run_analysis(tweet)

    result_list = manager.get_result_list()
    for result in result_list:
        print "[%s] %s" % (result[1], result[0])

if __name__ == "__main__":
    main_exec()
