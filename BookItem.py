class BookItem:
    def __init__(self, receipt_id, book_id, amount):
        self.receipt_id = receipt_id
        self.book_id = book_id
        self.amount = amount



    @staticmethod
    def showAll(db):
        cursor = db.cursor()
        sql = "SELECT * FROM book_item"
        cursor.execute(sql, )
        result = cursor.fetchall()
        return result

    @staticmethod
    def get(receipt_id, book_id, db):
        cursor = db.cursor()
        sql = "SELECT * FROM book_item WHERE receipt_id = %s AND book_id = %s"
        val = (receipt_id, book_id)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        return result

    def add(self, db):
        cursor = db.cursor()
        sql = "INSERT INTO book_item (receipt_id, book_id, amount) VALUES (%s, %s, %s)"
        val = (self.receipt_id, self.book_id, self.amount)
        cursor.execute(sql, val)
        db.commit()