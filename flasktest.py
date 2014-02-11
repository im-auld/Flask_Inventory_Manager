#Author: Ian Auld
#Date: '1/15/14'
#PyVer: 2.7
#Title: 'Flask_Inventory_Manager'
#Description:

from flask import Flask, render_template, request
from forms import ItemForm, ShelfForm, BinForm, SearchForm, StockForm 
from models import Item, Bin, Shelf, BinItem, db, query_all
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
    context = {
        'stock_form' : stock_form,
        'bin_list' : bin_list,
        'item_list' : item_list,
        'shelf_list' : shelf_list,
        'bin_item_list' : bin_item_list,
    }
    if request.method == 'GET':
        # return render_template('home.html', **context)
        return render_template('home.html', stock_form=stock_form, bin_list=bin_list, item_list=item_list, shelf_list=shelf_list, bin_item_list=bin_item_list)
    else:
        if stock_form.validate():
            new_bi = BinItem(stock_form.bin.data, stock_form.item.data, stock_form.qty.data)
            db.session.add(new_bi)
            db.session.commit()
            print(new_bi.bin_id, new_bi.item_id, new_bi.qty)
            return render_template('home.html', 
                stock_form=stock_form, 
                bin_list=bin_list, 
                item_list=item_list, 
                shelf_list=shelf_list, 
                bin_item_list=bin_item_list, 
                success=True
            )
        else:
            return render_template('home.html', 
                stock_form=stock_form, 
                bin_list=bin_list, 
                item_list=item_list, 
                shelf_list=shelf_list, 
                bin_item_list=bin_item_list, 
                success=False
            )

def stock_adjust(item_id, bin_id, qty):
    adjust = db.session.query(BinItem).filter(BinItem.bin_id == bin_id).filter(BinItem.item_id == item_id).one()
    if adjust:
        adjust.qty += qty
    else:
        new_bi = BinItem(bin_id, item_id, qty)
        db.session.add(new_bi)
    db.session.commit()
    

@app.route('/items', methods=['GET', 'POST'])
def items():
    try:
        log.info('Start reading from DB')
        i_form = ItemForm()
        s_form = SearchForm()
        item_list = db.session.query(Item).all()
        if request.method == 'GET':
            return render_template('items.html', i_form=i_form, s_form=s_form, item_list=item_list)
        else:
            if i_form.validate():
                new_item = Item(i_form.sku.data, i_form.title.data)
                db.session.add(new_item)
                db.session.commit()
                i_form.sku.data = ''
                i_form.title.data = ''
                item_list = db.session.query(Item).all()
                return render_template('items.html', i_form=i_form, s_form=s_form, item_list=item_list, item_added=True)
            else:
                return render_template('items.html', i_form=i_form, s_form=s_form, item_list=item_list, item_added=False)
    except:
        _, ex, _ = sys.exc_info()
        log.error(ex.message)
        return render_template('items.html', i_form=i_form, s_form=s_form, item_list=item_list)


@app.route('/shelves', methods=['GET', 'POST'])
def shelves():
    form = ShelfForm()
    shelf_list = db.session.query(Shelf).all()
    if request.method == 'GET':
        return render_template('shelves.html', form=form, shelf_list=shelf_list)
    else:
        if form.validate():
            new_shelf = Shelf(form.name.data)
            db.session.add(new_shelf)
            db.session.commit()
            form.name.data = ''
            return render_template('shelves.html', form=form, shelf_list=shelf_list, shelf_added=True)
        else:
            return render_template('shelves.html', form=form, shelf_list=shelf_list, shelf_added=False)


@app.route('/bins', methods=['GET', 'POST'])
def bins():
    form = BinForm()
    bin_list = db.session.query(Bin).all()
    if request.method == 'GET':
        return render_template('bins.html', form=form, bin_list=bin_list)
    else:
        if form.validate():
            new_bin = Bin(form.name.data, 1)  #TODO: Fix this. Need to get the shelf_id from the shelf_name
            db.session.add(new_bin)
            db.session.commit()
            form.name.data = ''
            form.shelf_name = ''
            return render_template('bins.html', form=form, bin_list=bin_list, shelf_added=True)
        else:
            return render_template('bins.html', form=form, bin_list=bin_list, shelf_added=False)


if __name__ == '__main__':
    app.run(debug=True)
