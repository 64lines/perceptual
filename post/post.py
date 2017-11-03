from database.database import DatabaseManager
from settings import UPDATE_ENTRY
from settings import QUERY_ENTRIES

# Post Object
class Post():
    def __init__(self):
        self.id = 0
        self.post_text = ""

class PostManager():
    def add_analysis_record(self, id_post, polarity):
        db_manager = DatabaseManager()
        db_manager.open_connection()

        record_update = UPDATE_ENTRY.format(id_post, polarity)

        cursor = db_manager.connection.cursor()
        cursor.execute(record_update)

        db_manager.commit()
        db_manager.close_connection()

    def get_entries(self):
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
            list_entries.append(post)

        db_manager.close_connection()
        return list_entries