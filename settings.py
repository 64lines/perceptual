NLTK_API_URL = "http://text-processing.com/api/sentiment/"
POSITIVE_WORDS_PATH = "inputs/positive_words_es.txt"
NEGATIVE_WORDS_PATH = "inputs/negative_words_es.txt"

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
QUERY_ENTRIES = 'SELECT id, tweet, reviewed FROM tweet_post WHERE reviewed=false'
