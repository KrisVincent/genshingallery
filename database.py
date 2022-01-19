from flask import Flask,redirect,url_for,render_template ,request,session,flash

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "y@m3T32"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///genshin_Log.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class account_table(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name  = db.Column(db.String(100))
    email  = db.Column(db.String(100))
    gender  = db.Column(db.String(100))

    def __init__(self, username,fname,lname,email,gender, password):
        self.username = username
        self.first_name = fname
        self.last_name = lname
        self.email = email
        self.gender = gender
        self.password = password


class gallery_account_table(db.Model):

    gallery_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer)

    def __init__(self, account_id):
        self.account_id = account_id


class mondstadt(db.Model):

    input_id = db.Column(db.Integer, primary_key=True)
    gallery_id = db.Column(db.Integer)
    images = db.Column(db.LargeBinary)
    region = db.Column(db.String(100))
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __init__(self, gallery_id, images,region, name, description):
        self.gallery_id = gallery_id
        self.images = images
        self.region = region
        self.name = name
        self.description = description


class inazuma(db.Model):

    input_id = db.Column(db.Integer, primary_key=True)
    gallery_id = db.Column(db.Integer)
    images = db.Column(db.LargeBinary)
    region = db.Column(db.String(100))
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __init__(self, gallery_id, images,region, name, description):
        self.gallery_id = gallery_id
        self.images = images
        self.region = region
        self.name = name
        self.description = description


class liyue(db.Model):

    input_id = db.Column(db.Integer, primary_key=True)
    gallery_id = db.Column(db.Integer)
    images = db.Column(db.LargeBinary)
    region = db.Column(db.String(100))
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __init__(self, gallery_id, images,region, name, description):
        self.gallery_id = gallery_id
        self.images = images
        self.region = region
        self.name = name
        self.description = description

class characters(db.Model):

    input_id = db.Column(db.Integer, primary_key=True)
    gallery_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    region = db.Column(db.String(100))
    vision = db.Column(db.String(100))
    portrait = db.Column(db.LargeBinary)

    def __init__(self, gallery_id, name, description, portrait,vision,region):
        self.gallery_id = gallery_id
        self.portrait = portrait
        self.name = name
        self.description = description
        self.vision = vision
        self.region = region
