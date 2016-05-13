from settings import POSITIVE_WORDS_PATH, NEGATIVE_WORDS_PATH
from utils import get_file_lines

# Looks for emoticons to figure out more quickly the
# sentiment of the tweet.
class EmoticonAnalyzer:
    def __init__(self):
        self.__dict_emoticon = {
            "positive": [":-P", ";-)", ":-D", ":-)", ":D", ":)", "xD"],
            "negative": [":-||", ":-/", "D-:", ":-(", "D:", ":(", "Dx"]
        }

    def analyze_text(self, text):
        positive_index = 0
        negative_index = 0
        result = ""

        for emoticon in self.__dict_emoticon["positive"]:
            if emoticon in text:
                positive_index += 1

        for emoticon in self.__dict_emoticon["negative"]:
            if emoticon in text:
                negative_index += 1

        if positive_index > negative_index:
            result = "positive"
        elif negative_index > positive_index:
            result = "negative"
        elif negative_index == positive_index:
            result = "neutral"

        return result

class BagOfWordsAnalizer:
    def __init__(self):
        self.list_positive_words = []
        self.list_negative_words = []
        self.__polarities = {
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }

    def analyze_text(self, text):
        result = ""

        list_words = text.split(" ")
        for word in list_words:
            word = word.lower()
            if word in self.list_positive_words:
                self.__polarities["positive"] += 1
            elif word in self.list_negative_words:
                self.__polarities["negative"] += 1
            else:
                self.__polarities["neutral"] += 1

        if self.__polarities["positive"] > self.__polarities["negative"]:
            result = "positive"
        elif self.__polarities["positive"] < self.__polarities["negative"]:
            result = "negative"
        else:
            result = "neutral"

        return result

# Bag of words models using positive, negative and
# neutral statuses.
class OpinionMiningAnalyzer:
    def __init__(self):
        self.__list_positive_words = get_file_lines(POSITIVE_WORDS_PATH)
        self.__list_negative_words = get_file_lines(NEGATIVE_WORDS_PATH)

        # List of entries to evaluate
        self.list_entries = []

        # Analysis result, this should be checked after the analysis has been made.
        self.analysis_result = {"positive": 0, "negative": 0, "neutral": 0}

    def analyize_entries(self):
        for entry in self.list_entries:
            self.make_analysis(entry)

    # Make general analysis of all the texts evaluated.
    def make_analysis(self, text):
        # Emoticon analysis
        emo_analyzer = EmoticonAnalyzer()
        bow_result = emo_analyzer.analyze_text(text)

        # Bag of words analysis
        bow_analyzer = BagOfWordsAnalizer()
        bow_analyzer.list_positive_words = self.__list_positive_words
        bow_analyzer.list_negative_words = self.__list_negative_words
        emo_result = bow_analyzer.analyze_text(text)

        if emo_result is not 'neutral':
            self.analysis_result[emo_result] += 1
        else:
            self.analysis_result[bow_result] += 1
