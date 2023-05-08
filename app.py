from flask import Flask, render_template, request, redirect, url_for
from Book import Book
import mysql.connector,datetime

app = Flask(__name__)

# Thiết lập kết nối đến cơ sở dữ liệu
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="db"
)

@app.route("/")
def home():
    # Lấy số trang hiện tại từ query string, mặc định là 1 nếu không có
    page = int(request.args.get('page', 1))

    # Tính toán vị trí bắt đầu và kết thúc của danh sách sách trên trang
    per_page = 10
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    # Lấy danh sách các cuốn sách trong khoảng thời gian từ start_index đến end_index
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM books LIMIT {start_index}, {per_page}")
    books = cursor.fetchall()
    cursor.execute(f"SELECT DISTINCT genre FROM books ORDER BY genre asc")
    genres = cursor.fetchall()  
    return render_template("index.html", books=books, page=page, len=len(books), genres=genres, genreSize=len(genres))

@app.route("/search")
def search():
    # Lấy từ khóa tìm kiếm từ query string
    keyword = request.args.get("keyword")

    # Tìm kiếm các cuốn sách chứa từ khóa
    books = Book.search(keyword, db)

    return render_template("search.html", keyword=keyword, books=books)

@app.route("/filter")
def filter():
    page = int(request.args.get('page', 1))
    # Tính toán vị trí bắt đầu và kết thúc của danh sách sách trên trang
    per_page = 10
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    # Lấy thể loại sách từ query string
    genre = request.args.get("genre")
    if(genre!="All Genres"):
        filteredBooks = Book.filter(genre, db)
        # Lọc các cuốn sách theo thể loại
        cursor = db.cursor()
        cursor.execute(f"SELECT DISTINCT genre FROM books ORDER BY genre asc")
        genres = cursor.fetchall()
        result= {}
        result['books']=filteredBooks
        result['len']=len(filteredBooks)
        result['genres']=genres
        result['genreSize']=1
        result['page']=page
        return result
    else:
        print("))))))))))))))))--)))))))")
        return redirect(url_for('home'))

@app.route("/sort")
def sort():
    # Lấy tiêu chí sắp xếp từ query string
    sort_by = request.args.get("sort_by")

    # Sắp xếp danh sách các cuốn sách theo tiêu chí
    sorted_books = Book.sort(sort_by, db)

    return render_template("sort.html", sort_by=sort_by, books=sorted_books)

@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Get the form data from the request object
        title = request.form['title']
        print(request.form['author'])
        author = request.form['author']
        shelf_id = request.form['shelf_id']
        genre = request.form['genre']
        code = request.form['code']
        amount = request.form['amount']

        # Create a Book object and add the new book to the database

        Book.add(Book(title, author, shelf_id, genre, None, code, amount, 0),db)

        # Redirect to the home page after adding the book
        return redirect(url_for('home'))
    else:
        return render_template('add.html',books=None, page=None, len=0, genres=None, genreSize=0)
    
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    book = Book.query.get(id)

    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        book.code = request.form['code']
        book.amount = request.form['amount']
        book.occupancy = request.form['occupancy']

        # update the book in the database
        db.session.commit()

        # redirect to the home page
        return redirect(url_for('home'))

    return render_template('edit.html', book=book)

# define the route for the delete book page
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    book = Book.query.get(id)

    # delete the book from the database
    db.session.delete(book)
    db.session.commit()

    # redirect to the home page
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
