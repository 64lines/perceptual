NLTK_API_URL = "http://text-processing.com/api/sentiment/"
POSITIVE_WORDS_PATH = "inputs/positive_words_es.txt"
NEGATIVE_WORDS_PATH = "inputs/negative_words_es.txt"

USE_DB=False

# Database connection info.
DB_USER = "urbana"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_PASSWORD = "urbana"
DB_INSTANCE = "urbana_database"
DB_POST_FIELD = "tweet"
DB_POST_TABLE = "tweet_post"
DB_RESULTS_TABLE = ""


# Queries
INSERT_ENTRY = "insert into post_analysis (id_post, polarity)  values (%s, '%s')"
QUERY_ENTRIES = 'SELECT t.id, t.tweet FROM tweet_post t WHERE t.id not in (SELECT a.id_post FROM post_analysis a)'
