from settings import DB_PORT
from settings import DB_HOST
from settings import DB_USER
from settings import DB_ENGINE
from settings import DB_PASSWORD
from settings import DB_INSTANCE

# Database operations.
class DatabaseManager():
    def __init__(self):
        self.connection = None

    def open_connection(self):
        import sys
        if DB_ENGINE == 'mysql':
            import MySQLdb

            try:
                self.connection = MySQLdb.connect(
                    db=DB_INSTANCE,
                    user=DB_USER,
                    passwd=DB_PASSWORD,
                    host=DB_HOST
                )
            except Exception, e:
                print 'Error connecting to MySQL database, cause: %s' % e
                sys.exit(1)
        elif DB_ENGINE == 'postgres':
            import psycopg2

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