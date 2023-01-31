from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from info import get_isbninfo, get_isbninfo_from_image
search_books = []

app = Flask(__name__)

# sqlalchemy config
# SQLALCHEMY_DATABASE_URI = "sqlite:///" +os.path.join(basedir, "app.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///username.db" # "sqlite://
app.config["AQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.jinja_env.auto_reload =True
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQLAlchemy(app)
# db.init_app(app)

from model import Book


#  sqlite:///:memory: (or, sqlite://)
#  sqlite:///relative/path/to/file.db
#  sqlite:////absolute/path/to/file.db
# "sqlite:///database.db" # sqlite:/home/isbn/instance/database.db ???
# "sqlite://tmp/test.db" # sqlite://tmp//home/isbn/instance/test.db
# "sqlite://root@127.0.0.1" # sqlite://root@127.0.0.1//home/isbn//instance
# "sqlite://root@127.0.0.1/test.db" # sqlite://root@127.0.0.1//home/isbn/instance/test.db

######################################################################
@app.before_first_request
def create_db():
    db.create_all()
    
# def delete_user():
#     db.drop_all()
######################################################################
# TODO: view
@app.route("/", methods=["GET"])
def home_view():
    global search_books
    # search_books = [] # ???
    db_books = Book.get_allbooks_in_db()
    # stored_books=[]
    return render_template("home.html", search_books=search_books, db_books=db_books)

@app.route("/searchbook", methods=["POST"])
def search_books_view():
    global search_books
    book_name = request.values["bookname"]
    barcode_file = request.files["barcodefile"]
    if barcode_file.filename != "":
        book_isbn = get_isbninfo_from_image(barcode_file)
    else:
        book_name = request.values["bookname"]
        book_isbn = request.values["bookisbn"]
    search_books = get_isbninfo(book_name, book_isbn)
    print("name: ",book_name, " isbn: ",book_isbn) 

    if not search_books:
        # alert
        print("not found")
    else:
        # print("search_books", search_books)
        pass    
    
    return redirect(url_for("home_view"))


@app.route("/addbook", methods=["POST"])
def add_book_view():
    global search_books
    book_number = int(request.values["addbook_number"])
    # save data
    book_info_dict = search_books[book_number-1]
    book_info = Book(book_info_dict["book_name"], 
                    book_info_dict["book_author"],
                    book_info_dict["book_publisher"],
                    # book_info_dict["book_cost"],
                    # book_info_dict["book_other"],
                    None,
                    None,
                    book_info_dict["book_isbn"])


    print("\nAdd")
    print(book_info)

    book_now = Book.add_book_to_db(book_info)
    print("Add Search Book:", book_now)
    
    # book_info = Book(book_name, book_isbn)
    # add_book(book_info)
    return redirect(url_for("home_view"))

@app.route("/manualinputbook", methods=["POST"])
def manual_input_book_view():
    book_name = request.values["bookname"]
    book_author = request.values["bookauthor"]
    book_publisher = request.values["bookpublisher"]
    book_cost = request.values["bookcost"]
    book_other = request.values["bookother"]
    book_info = Book(book_name, book_author,book_publisher,
                    book_cost, book_other, None)
    book_now = Book.add_book_to_db(book_info)
    print("Add Manualinput Book: ", book_now)
    return redirect(url_for("home_view"))

@app.route("/deletedbbook", methods=["POST"])
def delete_db_book_view():
    id = int(request.values["deletedbbook_id"])
    book_now = Book.delete_book_to_db(id)
    print("Delete Database Book: ", book_now)
    return redirect(url_for("home_view"))


@app.route("/modifydbbook", methods=["POST"])
def modify_db_book_view():
    
    type = request.values["type"]
    if type == "input":
        print(request.form)
        id = int(request.values["id"])
        book_name = request.values["bookname"]
        book_author = request.values["bookauthor"]
        book_publisher = request.values["bookpublisher"]
        book_cost = request.values["bookcost"]
        book_other = request.values["bookother"]
        book_info = {"book_name": book_name, "book_author": book_author,"book_publisher": book_publisher,
                    "book_cost": book_cost, "book_other": book_other}

        
        book_now = Book.update_book_in_db(id, book_info)
        print("Modify Database Book: ", book_now)

    return redirect(url_for("home_view"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port="77")


    