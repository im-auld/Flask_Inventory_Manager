#Author: Ian Auld
#Date: '1/15/14'
#PyVer: 2.7
#Title: 'Flask_Inventory_Manager'
#Description:

from flask import Flask, render_template, request, redirect, url_for
from forms import ItemForm, ShelfForm, BinForm, SearchForm, StockForm 
from models import Item, Bin, Shelf, BinItem, db, query_all
from sqlalchemy.orm.exc import NoResultFound
import os
import logging
import sys


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///inventory.db')
app.secret_key = 'secret_shhhhh!@#$1234'
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    item_list = query_all(Item)
    shelf_list = query_all(Shelf)
    bin_list = query_all(Bin)
    bin_item_list = query_all(BinItem)
    stock_form = StockForm()
    stock_form.item.choices = [(c.item_id, c.sku) for c in Item.query.order_by('sku')]
    stock_form.bin.choices = [(c.bin_id, c.name) for c in Bin.query.order_by('name')]
    if stock_form.validate_on_submit():
        try:
            bi = db.session.query(BinItem)\
                .filter(BinItem.item_id == stock_form.item.data)\
                .filter(BinItem.bin_id == stock_form.bin.data).one()
        except NoResultFound:
            new_bi = BinItem(stock_form.bin.data, stock_form.item.data, stock_form.qty.data)
            db.session.add(new_bi)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            if stock_form.in_out.data == 'in':
                bi.qty += stock_form.qty.data
            else:
                bi.qty -= stock_form.qty.data
            db.session.commit()
            return redirect(url_for('home'))
    else:
        print 'it failed!'
    stock_form.qty.data = None
    return render_template('home.html',
                           stock_form=stock_form,
                           bin_list=bin_list,
                           item_list=item_list,
                           shelf_list=shelf_list,
                           bin_item_list=bin_item_list)


@app.route('/items', methods=['GET', 'POST'])
def items():
    try:
        log.info('Start reading from DB')
        i_form = ItemForm()
        s_form = SearchForm()
        item_list = db.session.query(Item).all()
        if i_form.validate_on_submit():
            new_item = Item(i_form.sku.data, i_form.title.data)
            db.session.add(new_item)
            db.session.commit()
            i_form.sku.data = ''
            i_form.title.data = ''
            item_list = db.session.query(Item).all()
            return redirect(url_for('items'))
        return render_template('items.html', i_form=i_form, s_form=s_form, item_list=item_list)
    except:
        _, ex, _ = sys.exc_info()
        log.error(ex.message)
        return render_template('items.html', i_form=i_form, s_form=s_form, item_list=item_list)


@app.route('/shelves', methods=['GET', 'POST'])
def shelves():
    form = ShelfForm()
    shelf_list = db.session.query(Shelf).all()
    if form.validate_on_submit():
        new_shelf = Shelf(form.name.data)
        db.session.add(new_shelf)
        db.session.commit()
        form.name.data = ''
        return redirect(url_for('shelves'))
    return render_template('shelves.html', form=form, shelf_list=shelf_list)


@app.route('/bins', methods=['GET', 'POST'])
def bins():
    form = BinForm()
    form.shelf_name.choices = [(c.shelf_id, c.name) for c in Shelf.query.order_by('name')]
    bin_list = db.session.query(Bin).all()
    if form.validate_on_submit():
        new_bin = Bin(form.name.data, form.shelf_name.data)
        db.session.add(new_bin)
        db.session.commit()
        form.name.data = ''
        form.shelf_name = ''
        return redirect(url_for('bins'))
    return render_template('bins.html', form=form, bin_list=bin_list)

# TODO: Add delete method
# TODO: Add item edit method

if __name__ == '__main__':
    app.run(debug=True)
