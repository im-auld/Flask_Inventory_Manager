#Author: Ian Auld
#Date: '1/15/14'
#PyVer: 2.7
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

    def get_shelf_name(self):
        shelf = db.session.query(Shelf).filter(Shelf.shelf_id == self.shelf_id).one()
        return shelf

class BinItem(db.Model):
    __tablename__ = 'bin_item'
    bin_id = db.Column(db.Integer, db.ForeignKey('bin.bin_id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    total_qty = 0

    def __init__(self, bin_id, item_id, qty):
        self.bin_id = bin_id
        self.item_id = item_id
        self.qty = qty
        
        
    def get_item(self):
        item = db.session.query(Item).filter(Item.item_id == self.item_id).one()
        return item
        
        
    def get_bin(self):
        bin = db.session.query(Bin).filter(Bin.bin_id == self.bin_id).one()
        return bin
        
        
    def get_item_total(self):
        total = 0
        results = db.session.query(BinItem).all()
        for row in results:
            total += row.qty
        return total


def query_all(model):
    result = db.session.query(model).all()
    return result

