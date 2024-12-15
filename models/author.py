# Import the get_db_connection function from the database.connection module
from database.connection import get_db_connection

class Author:
    def __init__(self, id, name=None):
        self._id = id
        if name is not None:
            self._name = name
        else:
            self._name = None

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        if self._name is None:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM authors WHERE id = ?', (self._id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._name = result[0]
            else:
                raise ValueError("Name not found in database")
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if len(value) == 0:
            raise ValueError("Name must be longer than 0 characters")
        self._name = value
    
    
    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article[0], article[1], article[2], article[3], article[4]) for article in articles]
    

    def magazines(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.id, magazines.name, magazines.category 
            FROM magazines
            INNER JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self._id,))
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(magazine[0], magazine[1], magazine[2]) for magazine in magazines]
    
    def __repr__(self):
        return f'<Author {self.name}>'
