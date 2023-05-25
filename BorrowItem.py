class BorrowItem:
    def __init__(self, borrow_id, book_id, amount, status, return_date):
        self.borrow_id = borrow_id
        self.book_id = book_id
        self.amount = amount
        self.status = status
        self.return_date = return_date

    @staticmethod
    def showAll(db):
        cursor = db.cursor()
        sql = "SELECT * FROM borrow_item"
        cursor.execute(sql, )
        result = cursor.fetchall()
        return result

    @staticmethod
    def get(id, db):
        cursor = db.cursor()
        sql = "SELECT * FROM borrow_item WHERE borrow_id = %s"
        val = (id, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        return result

    def add(self, db):
        cursor = db.cursor()
        sql = "INSERT INTO borrow_item (borrow_id, book_id, amount, status) VALUES (%s, %s, 1, 0)"
        val = (self.borrow_id, self.book_id)
        cursor.execute(sql, val)
        db.commit()