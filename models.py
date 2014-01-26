#Author: Ian Auld
#Date: '1/15/14'
#PyVer: 3.3
#Title: 'Flask_Inventory_Manager'
#Description:


from sqlalchemy.ext.declarative import declarative_base
from flask.ext.sqlalchemy import SQLAlchemy


Base = declarative_base()
db = SQLAlchemy()


class Shelf(db.Model):
    __tablename__ = 'shelf'
    shelf_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)

    def __init__(self, name):
        self.name = name


class Item(db.Model):
    __tablename__ = 'item'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sku = db.Column(db.String(50), nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)

    def __init__(self, sku, title):
        self.sku = sku
        self.title = title


class Bin(db.Model):
    __tablename__ = 'bin'
    bin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.shelf_id'))

    def __init__(self, name, shelf_id):
        self.name = name
        self.shelf_id = shelf_id


class BinItem(db.Model):
    __tablename__ = 'bin_item'
    bin_id = db.Column(db.Integer, db.ForeignKey('bin.bin_id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), primary_key=True)
    qty = db.Column(db.Integer, nullable=False)

    def __init__(self, bin_id, item_id, qty):
        self.bin_id = bin_id
        self.item_id = item_id
        self.qty = qty



