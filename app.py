from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config.update(
    SECRET_KEY='topsecret',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:mb121691@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db = SQLAlchemy(app)

@app.route('/index')
@app.route('/')
def index():
    return "Hello World!"

@app.route('/new/')
def query_strings(greeting = "hello"):
    query_val = request.args.get('greeting', greeting)
    return '<h1> the greeting is : {0} </h1>'.format(query_val)

@app.route('/user/')
@app.route('/user/<name>')
def no_query_strings(name = "Maged"):
    return '<h1> Hello {} </h1>'.format(name)

@app.route('/number/<int:num>')
def number_function(num):
    return '<h1> this number is: {}</h1>'.format(num)

@app.route('/html')
def html():
    return render_template('hello.html')

@app.route('/movies')
def watch_movies():
    movies_list = [ 'Stranger With Tentacles', 'Spy Of Our Ship',
    'Intruder Of Our Ship',
    'Volunteer Of The Past',
    'Emperors Of New Earth',
    'Defenders With Four Eyes',
    'Droids Of The Vacuum','Figures']
    return render_template('movies.html', movies=movies_list, name="Maged")

@app.route('/tables')
def table_movies():
    movies_dic = {'Stranger With Tentacles': 1.2, 'Spy Of Our Ship': 2.3,
    'Intruder Of Our Ship': 2.0,
    'Volunteer Of The Past': 1.5,
    'Emperors Of New Earth': 3.1,
    'Defenders With Four Eyes': 1.7,
    'Droids Of The Vacuum': 1.9,'Figures': 2.5}

    return render_template('tables.html', movies=movies_dic, name='Maged')
@app.route('/filters')
def filter_data():
    movies_dic={'Stranger With Tentacles': 1.2, 'Spy Of Our Ship': 2.3,
    'Intruder Of Our Ship': 2.0,
    'Volunteer Of The Past': 1.5,
    'Emperors Of New Earth': 3.1,
    'Defenders With Four Eyes': 1.7,
    'Droids Of The Vacuum': 1.9,'Figures': 2.5
    }

    return render_template('filter.html', movies=movies_dic, name=None, film='a christmas carol')

@app.route('/macros')
def macros():
    movies_dict={
        'Stranger With Tentacles': 1.2, 'Spy Of Our Ship': 2.3,
    'Intruder Of Our Ship': 2.0,
    'Volunteer Of The Past': 1.5,
    'Emperors Of New Earth': 3.1,
    'Defenders With Four Eyes': 1.7,
    'Droids Of The Vacuum': 1.9,'Figures': 2.5
    }

    return render_template('using_macros.html', movies=movies_dict)

class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return ' Name is {}'.format( self.name)

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
    
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)

if __name__ == '__main':
    db.create_all()
    app.run(debug=True)