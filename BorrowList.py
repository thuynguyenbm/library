class BorrowList:
    def __init__(self, borrow_id, student_id, borrow_date, due_date, user_id):
        self.borrow_id = borrow_id
        self.student_id = student_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.user_id = user_id


    @staticmethod
    def showAll(db):
        cursor = db.cursor()
        sql = "SELECT * FROM borrow_order_list"
        cursor.execute(sql, )
        result = cursor.fetchall()
        return result

    @staticmethod
    def get(id, db):
        cursor = db.cursor()
        sql = "SELECT * FROM borrow_order_list WHERE borrow_id = %s"
        val = (id, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        return result

    def add(self, db):
        cursor = db.cursor()
        sql = "INSERT INTO borrow_order_list (student_id, borrow_date, due_date, user_id) VALUES (%s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY), %s)"
        val = (self.student_id, self.user_id)
        cursor.execute(sql, val)
        db.commit()