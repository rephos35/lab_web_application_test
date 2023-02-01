# from __main__ import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from main import db, app
# db.init_app(app)

class Book(db.Model):
    __tablename__ = "username"
    # , unique=True, unllable=False, default="/"
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), nullable=False) # nullable???
    book_author = db.Column(db.String(20)) 
    book_publisher = db.Column(db.String(40)) 
    book_cost = db.Column(db.String(20))
    book_other = db.Column(db.String(80))
    book_isbn = db.Column(db.Integer)
    createtime = db.Column(db.DateTime, default = datetime.now().date())
    # updatetime = db.Column(db.DateTime, default=datetime.now().date(), comment="修改時間")

    def __init__(self, book_name, book_author=None, book_publisher=None, book_cost=None, book_other=None, book_isbn=None):
        self.book_name = book_name
        self.book_author = book_author
        self.book_publisher = book_publisher
        self.book_cost = book_cost
        self.book_other = book_other
        self.book_isbn = book_isbn

    def __repr__(self):
        return "{ id: %r, book_name: %r, book_author: %r, book_publisher: %r, book_cost: %r, book_other: %r, book_isbn: %r }" %(self.id, self.book_name, self.book_author, self.book_publisher, self.book_cost, self.book_other, self.book_isbn)

    def add_book_to_db(book_info):
        db.session.add(book_info)
        db.session.commit()
        return book_info

    def delete_book_to_db(id):
        # book_info = Book.query.get(id)
        # book_info = Book.query.filter_by(id=id).one()
        book_info = Book.query.filter(Book.id==id).one()
        db.session.delete(book_info)
        db.session.commit()
        return book_info

    def update_book_in_db(id, book_info):
        # db.session.query(Book).filter(Book.id==id).update(book_info)
        book = Book.query.filter(Book.id==id)
        book.update(book_info)
        book_info = book.one()
        db.session.commit()
        return book_info
        
    def get_allbooks_in_db():
        # Book.query.all()
        return db.session.query(Book).all()

    # def find_book_in_db(book_info):
    #     return Book.session.filter_by(user_name=book_info.username).all()


    # book = Book.query.get(id)
    # book = Book.query.filter_by(user_name=book_info.username).one()
    # book = Book.query.filter_by(user_name=book_info.username).one_or_404(description=f"No user named {username}")
    # book = Book.query(Book.id==id).first()
    # db.session.query(Book).filter(Book.id==ids).delete() #batch
    # db.session.execute(select())


