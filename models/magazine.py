# Import the get_db_connection function from the database.connection module
from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category

    @property
    def id(self):
        return self._id
    
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value

    
    @property
    def category(self):
        return self._category
    
    
    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise ValueError("Category must be a string")
        if len(value) <= 0:
            raise ValueError("Category must be longer than 0 characters")
        self._category = value
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (value, self._id))
        conn.commit()
        conn.close()

    
    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, content, author_id, magazine_id FROM articles
            WHERE magazine_id = ?
        ''', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article[0], article[1], article[2], article[3], article[4]) for article in articles]
    
    def contributors(self):
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.id, authors.name FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self._id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author[0], author[1]) for author in authors]

    
    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self._id,))
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return titles
    
    def contributing_authors(self):
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.id, authors.name, COUNT(articles.id) as article_count FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        ''', (self._id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author[0], author[1]) for author in authors]

    def __repr__(self):
        return f'<Magazine {self.name}>'
