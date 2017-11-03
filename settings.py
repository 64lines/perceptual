USE_DB=False

# Database connection info.
DB_ENGINE = "mysql" # Could be 'mysql' or 'postgres'
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_PASSWORD = "liferay"
DB_INSTANCE = "lportal"
DB_RESULTS_TABLE = ""

# Queries
UPDATE_ENTRY = "update vz_urbanatweet set polaridad='{1}' where urbanatweetid='{0}'"
QUERY_ENTRIES = 'SELECT t.urbanatweetid, t.text_ FROM vz_urbanatweet t WHERE t.polaridad is null'