import mysql.connector

class Book:
    def __init__(self, title, author, shelf_id, genre, date, code, amount, occupancy):
        self.title = title
        self.shelf_id = shelf_id
        self.author = author
        self.genre = genre
        self.date = date
        self.code = code
        self.amount = amount
        self.occupancy = occupancy

    def add(self, db):
        cursor = db.cursor()
        print(type(self.code))
        sql = "INSERT INTO books (title, author, shelf_id, genre, date, code, amount, occupancy) VALUES (%s, %s, %s, %s, now(), %s, %s, 0)"
        val = (self.title, self.author, self.shelf_id, self.genre, self.code, self.amount)
        
        cursor.execute(sql, val)
        db.commit()

    def delete(id, db):
        cursor = db.cursor()
        sql = "DELETE FROM books WHERE id = %s"
        val = (id,)
        cursor.execute(sql, val)
        db.commit()

    def update(self,id, db):
        cursor = db.cursor()
        sql = "UPDATE books SET title = %s, shelf_id = %s, author = %s, genre = %s, date = %s, code = %s, amount = %s, occupancy = %s WHERE id = %s"
        val = (self.title, self.shelf_id, self.author, self.genre, self.date, self.code, self.amount, self.occupancy, id)
        cursor.execute(sql, val)
        db.commit()

    @staticmethod
    def search(keyword, db):
        cursor = db.cursor()
        sql = "SELECT * FROM books WHERE title LIKE %s OR genre LIKE %s"
        val = ('%' + keyword + '%', '%' + keyword + '%')
        cursor.execute(sql, val)
        result = cursor.fetchall()
        return result
    
    @staticmethod
    def filter(genre, db):
        cursor = db.cursor()
        sql = "SELECT * FROM books WHERE genre = %s"
        val = (genre,)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        return result

    @staticmethod
    def sort(sort_by, db):
        cursor = db.cursor()
        if sort_by == "title":
            sql = "SELECT * FROM books ORDER BY title ASC"
        elif sort_by == "date":
            sql = "SELECT * FROM books ORDER BY date ASC"
        else:
            return None
        cursor.execute(sql)
        result = cursor.fetchall()
        return result