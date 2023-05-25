class Supplier:
    def __init__(self, supplier_id, name, phone_number):
        self.supplier_id = supplier_id
        self.name = name
        self.phone_number = phone_number

    @staticmethod
    def showAll(db):
        cursor = db.cursor()
        sql = "SELECT * FROM student"
        cursor.execute(sql, )
        result = cursor.fetchall()
        return result

    @staticmethod
    def get(id, db):
        cursor = db.cursor()
        sql = "SELECT * FROM student WHERE student_id = %s"
        val = (id, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        return result
    
    @staticmethod
    def getNameById(id, db):
        cursor = db.cursor()
        sql = "SELECT name FROM student WHERE student_id = %s"
        val = (id, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        return result[0]

    def add(self, db):
        cursor = db.cursor()
        sql = "INSERT INTO student (student_id, name, email) VALUES (%s, %s, %s)"
        val = (self.student_id, self.name, self.email)
        cursor.execute(sql, val)
        db.commit()