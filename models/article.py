# Import the get_db_connection function from the database.connection module
from database.connection import get_db_connection


class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        self.id = id
        self._title = title
        self._content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    
    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                    (self.title, self.content, self.author_id, self.magazine_id))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

   
    @property
    def title(self):
        if not hasattr(self, '_title') and self.id is not None:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM articles WHERE id = ?", (self.id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._title = result[0]
            else:
                raise ValueError("Title not found in database")
        return self._title

    
    @title.setter
    def title(self, value):
        if self._title is None:
            if isinstance(value, str) and 5 <= len(value) <= 50:
                self._title = value
            else:
                raise ValueError("Title must be a string and between 5 and 50 characters")
        else:
            raise ValueError("Title cannot be changed after it is set")

    
    @property
    def content(self):
        
        if not hasattr(self, '_content') and self.id is not None:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT content FROM articles WHERE id = ?", (self.id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._content = result[0]
            else:
                raise ValueError("Content not found in database")
        return self._content

    
    @content.setter
    def content(self, value):
        if self._content is None:
            if isinstance(value, str):
                self._content = value
            else:
                raise ValueError("Content must be a string")
        else:
            raise ValueError("Content cannot be changed after it is set")

    
    @property
    def author(self):
        
        if not hasattr(self, '_author') and self.id is not None:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT authors.name
                FROM articles
                INNER JOIN authors ON articles.author_id = authors.id
                WHERE articles.id = ?
            ''', (self.id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._author = result[0]
            else:
                raise ValueError("Author not found in database")
        return self._author

    @property
    def magazine(self):
        if not hasattr(self, '_magazine') and self.id is not None:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT magazines.name
                FROM articles
                INNER JOIN magazines ON articles.magazine_id = magazines.id
                WHERE articles.id = ?
            ''', (self.id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._magazine = result[0]
            else:
                raise ValueError("Magazine not found in database")
        return self._magazine
    def __repr__(self):
        return f'<Article {self.title}>'

