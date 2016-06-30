import urllib
import psycopg2
from utils import get_file_lines
from settings import DB_PORT
from settings import DB_HOST
from settings import DB_USER
from settings import DB_PASSWORD
from settings import DB_INSTANCE
from settings import DB_POST_FIELD
from settings import DB_POST_TABLE
from settings import NLTK_API_URL
from settings import NEGATIVE_WORDS_PATH
from settings import POSITIVE_WORDS_PATH
from settings import QUERY_ENTRIES

# Post Object
class Post:
    def __init__(self):
        self.id = 0
        self.post_text = ""
        self.reviewed = ""

# Database operations.
class DatabaseManager:
    def __init__(self):
        self.connection = None

    def open_connection(self):
        try:
            self.connection = psycopg2.connect(
                database=DB_INSTANCE,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
            sys.exit(1)

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def commit(self):
        if self.connection:
            self.connection.commit()

class PostManager:
    def add_analysis_record(self, id_post, polarity):
        db_manager = DatabaseManager()
        db_manager.open_connection()

        record_insert = "insert into post_analysis (id_post, polarity)  values (%s, '%s')" % (id_post, polarity)

        cursor = db_manager.connection.cursor()
        cursor.execute(record_insert)

        db_manager.commit()
        db_manager.close_connection()

    def get_post_entries(self):
        list_entries = []

        db_manager = DatabaseManager()
        db_manager.open_connection()

        cursor = db_manager.connection.cursor()
        cursor.execute(QUERY_ENTRIES)
        list_data = cursor.fetchall()

        for row in list_data:
            post = Post()
            post.id = row[0]
            post.post_text = row[1]
            post.reviewed = row[2]
            list_entries.append(post)

        db_manager.close_connection()
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
        elif self.__polarities["negative"] > self.__polarities["positive"]:
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
            text = entry.post_text
            text = self.__format_text(text)
            polarity = self.make_analysis(text)
            print "[%s] - %s " % (polarity, text)

            manager = PostManager()
            manager.add_analysis_record(entry.id, polarity)

    def __format_text(self, text):
        text = text.strip().lower()

        # Converting hashtag to text.
        text = text.replace('#', '')

        # Removing literal marks.
        text = text.replace('?', '')
        text = text.replace('!', '')
        text = text.replace('.', '')
        text = text.replace(',', '')
        text = text.replace('\"', '')

        text = self.__remove_links(text)
        text = self.__remove_mentions(text)

        return text

    # Make general analysis of all the texts evaluated.
    def make_analysis(self, text):
        #print text

        # Emoticon analysis
        emo_analyzer = EmoticonAnalyzer()
        emo_result = emo_analyzer.analyze_text(text)

        # Bag of words analysis
        bow_analyzer = BagOfWordsAnalizer()
        bow_analyzer.list_positive_words = self.__list_positive_words
        bow_analyzer.list_negative_words = self.__list_negative_words
        bow_result = bow_analyzer.analyze_text(text)

        # NLTK analysis
        #nltk_analyzer = NLTKAnalyzer()
        #nltk_result = nltk_analyzer.analyze_text(text)

        # If the emoticon analysis is neutral then
        # use the bag of words analysis, if this analyisis is neutral too
        # then use the nltk analysis and if this analysis says that is neutral
        # too then use that one anyway.
        result = ""
        if emo_result is not 'neutral':
            self.analysis_result[emo_result] += 1
            result = emo_result
        else:
            self.analysis_result[bow_result] += 1
            result = bow_result
        #else:
        #    self.analysis_result[nltk_result] += 1
        #    result = nltk_result

        return result

    def __remove_links(self, text):
        list_words = text.split(' ')
        result_list = []
        for word in list_words:
            if not '://' in word:
                result_list.append(word)

        return ' '.join(result_list)

    def __remove_mentions(self, text):
        list_words = text.split(' ')
        result_list = []
        for word in list_words:
            if not '@' in word:
                result_list.append(word)

        return ' '.join(result_list)
