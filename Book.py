class Book:
    def __init__(self, id, title, author, location, genre, published_date, publishing_house, amount, occupancy):
        self.id = id
        self.title = title
        self.author = author
        self.location = location
        self.genre = genre
        self.published_date = published_date
        self.publishing_house = publishing_house
        self.amount = amount
        self.occupancy = occupancy

    @staticmethod
    def showAll(db):
        cursor = db.cursor()
        sql = "SELECT * FROM book"
        cursor.execute(sql, )
        result = cursor.fetchall()
        return result

    @staticmethod
    def get(id, db):
        cursor = db.cursor()
        sql = "SELECT * FROM book WHERE id = %s"
        val = (id, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        return result

    def add(self, db):
        cursor = db.cursor()
        sql = "INSERT INTO book (id, title, author, location, genre, published_date, publishing_house, amount, occupancy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0)"
        val = (self.id, self.title, self.author, self.location, self.genre, self.published_date, self.publishing_house, self.amount)
        
        cursor.execute(sql, val)
        db.commit()

    def delete(id, db):
        cursor = db.cursor()
        sql = "DELETE FROM book WHERE id = %s"
        val = (id,)
        cursor.execute(sql, val)
        db.commit()

    def update(self,id, db):
        cursor = db.cursor()
        sql = "UPDATE book SET title = %s, location = %s, author = %s, genre = %s, published_date = %s, publishing_house = %s, amount = %s, occupancy = %s WHERE id = %s"
        val = (self.title, self.location, self.author, self.genre, self.published_date, self.publishing_house, self.amount, self.occupancy, id)
        cursor.execute(sql, val)
        db.commit()

    @staticmethod
    def search(keyword, db):
        cursor = db.cursor()
        sql = "SELECT * FROM book WHERE title LIKE %s OR genre LIKE %s OR author LIKE %s"
        val = ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')
        cursor.execute(sql, val)
        result = cursor.fetchall()
        return result
    
    @staticmethod
    def filter(genre, db):
        cursor = db.cursor()
        sql = "SELECT * FROM book WHERE genre = %s"
        val = (genre,)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        return result

    @staticmethod
    def sort(sort_by, db):
        cursor = db.cursor()
        if sort_by == "title":
            sql = "SELECT * FROM book ORDER BY title ASC"
        elif sort_by == "date":
            sql = "SELECT * FROM book ORDER BY date ASC"
        else:
            return None
        cursor.execute(sql)
        result = cursor.fetchall()
        return result