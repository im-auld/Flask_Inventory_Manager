from flask import Flask, render_template, request
from forms import *
from models import Item, Bin, Shelf, BinItem, db
from flask.ext.sqlalchemy import SQLAlchemy
import os
import logging
import sys


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.secret_key = 'secret_shhhhh!@#$1234'
db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/items', methods=['GET', 'POST'])
def items():
    try:
        log.info('Start reading form DB')
        form = ItemForm()
        item_list = db.session.query(Item).all()
        if request.method == 'GET':
            return render_template('items.html', form=form, item_list=item_list)
        else:
            if form.validate():
                new_item = Item(form.sku.data, form.title.data)
                db.session.add(new_item)
                db.session.commit()
                form.sku.data = ''
                form.title.data = ''
                item_list = db.session.query(Item).all()
                return render_template('items.html', form=form, item_list=item_list, item_added=True)
            else:
                return render_template('items.html', form=form, item_list=item_list, item_added=False)
    except:
        _, ex, _ = sys.exc_info()
        log.error(ex.message)


@app.route('/shelves', methods=['GET', 'POST'])
def shelves():
    form = ShelfForm()
    shelf_list = db.session.query(Shelf).all()
    if request.method == 'GET':
        return render_template('shelves.html', form=form, shelf_list=shelf_list)
    else:
        if form.validate():
            shelf_list[form.name.data] = form.name.data
            form.name.data = ''
            return render_template('shelves.html', form=form, shelf_list=shelf_list, shelf_added=True)
        else:
            return render_template('shelves.html', form=form, shelf_list=shelf_list, shelf_added=False)


@app.route('/bins', methods=['GET', 'POST'])
def bins():
    form = BinForm()
    bin_list = db.session.query(Bin).all()
    if request.method == 'GET':
        return render_template('bins.html', form=form, bin_list=test_bin_dict)
    else:
        if form.validate():
            test_bin_dict[len(test_bin_dict) + 1] = form.name.data
            form.name.data = ''
            form.shelf_name = ''
            return render_template('bins.html', form=form, test_bin_dict=shelf_list, shelf_added=True)
        else:
            return render_template('bins.html', form=form, test_bin_dict=shelf_list, shelf_added=False)


if __name__ == '__main__':
    app.run(debug=True)
