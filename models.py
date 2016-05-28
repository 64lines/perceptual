import urllib
import psycopg2
from utils import get_file_lines
from settings import DB_USER
from settings import DB_PASSWORD
from settings import DB_INSTANCE
from settings import DB_POST_FIELD
from settings import DB_POST_TABLE
from settings import NLTK_API_URL
from settings import NEGATIVE_WORDS_PATH
from settings import POSITIVE_WORDS_PATH

# Database operations.
class DatabaseConnection:
    def get_post_entries(self):
        list_entries = []
        con = None
        try:
            con = psycopg2.connect(
                database=DB_INSTANCE,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cur = con.cursor()
            cur.execute(
                'SELECT %s FROM %s WHERE reviewed=false' %
                    (DB_POST_FIELD, DB_POST_TABLE)
            )
            list_data = cur.fetchall()
            list_entries = [post[0] for post in list_data]
            print list_entries
        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
            sys.exit(1)
        finally:
            if con:
                con.close()

        return list_entries

# Looks for emoticons to figure out more quickly the
# sentiment of the tweet.
class EmoticonAnalyzer:
    def __init__(self):
        self.__dict_emoticon = {
            "positive": [
                ":-)", ":)", ":D", ":o)", ":]", ":3", ":c)",
                ":>", "=]", "8)", "=)", ":}", ":^)", ":-D",
                "8-D", "8D", "x-D", "xD", "X-D", "XD", "=-D",
                "=D", "=-3", "=3", "B^D", ":-))", ":'-)",
                ":')", ";-)", ";)", "*-)", "*)", ";-]", ";]",
                ";D", ";^)", ":-,"
            ],
            "negative": [
                ":-||", ":-/", "D-:", ":-(", "D:", ":(", "Dx",
                ">:[", ":-(", ":(", ":-c", ":c", ":-<", ":<",
                ":-[", ":[", ":{", ";(", ":-||", ":@", ">:(",
                ":'-(", ":'(", ">:O", ":-O", ":O", ":-o", ":o",
                "8-0", "O_O", "o-o", "O_o", "o_O", "o_o", "O-O"
            ]
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

class NLTKAnalyzer:
    def __init__(self):
        self.__conventions = {
            "pos": "positive", "neg": "negative", "neutral": "neutral"
        }

    def analyze_text(self, text):
        data = urllib.urlencode({"text": text})
        u = urllib.urlopen(NLTK_API_URL, data)
        the_page = u.read()
        result = eval(the_page)['label']
        return self.__conventions[result]

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
            print self.analysis_result

    # Make general analysis of all the texts evaluated.
    def make_analysis(self, text):
        # Emoticon analysis
        emo_analyzer = EmoticonAnalyzer()
        emo_result = emo_analyzer.analyze_text(text)

        # Bag of words analysis
        bow_analyzer = BagOfWordsAnalizer()
        bow_analyzer.list_positive_words = self.__list_positive_words
        bow_analyzer.list_negative_words = self.__list_negative_words
        bow_result = bow_analyzer.analyze_text(text)

        # NLTK analysis
        nltk_analyzer = NLTKAnalyzer()
        nltk_result = nltk_analyzer.analyze_text(text)

        # If the emoticon analysis is neutral then
        # use the bag of words analysis, if this analyisis is neutral too
        # then use the nltk analysis and if this analysis says that is neutral
        # too then use that one anyway.
        if emo_result is not 'neutral':
            self.analysis_result[emo_result] += 1
        elif bow_result is not 'neutral':
            self.analysis_result[bow_result] += 1
        else:
            self.analysis_result[nltk_result] += 1
