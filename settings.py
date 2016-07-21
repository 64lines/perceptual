NLTK_API_URL = "http://text-processing.com/api/sentiment/"
POSITIVE_WORDS_PATH = "inputs/positive_words_es.txt"
NEGATIVE_WORDS_PATH = "inputs/negative_words_es.txt"

USE_DB=False

# Database connection info.
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_PASSWORD = "liferay"
DB_INSTANCE = "lportal"
DB_POST_FIELD = "text_"
DB_POST_TABLE = "vz_urbanatweet"
DB_RESULTS_TABLE = ""


# Queries
UPDATE_ENTRY = "update vz_urbanatweet set polaridad='{1}' where t.urbanatweetid='{0}'"
QUERY_ENTRIES = 'SELECT t.urbanatweetid, t.text_ FROM vz_urbanatweet t WHERE t.polaridad is null'