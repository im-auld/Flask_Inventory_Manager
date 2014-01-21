from flask import Flask, render_template, request
from forms import *
from models import *
from sqlalchemy.orm import sessionmaker
from flask.ext.sqlalchmey import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///inventory.db')
app.secret_key = 'secret_shhhhh!@#$1234'
app.debug = True  # TODO: IMPORTANT >> Remove this before pushing live!!!!!!

db = SQLAlchemy(app)

for i in range(100, 201):
    test_item_dict['SKU-{}'.format(i)] = 'Thing {}'.format(i)

test_shelf_dict = {}
for i in range(1, 21):
    test_shelf_dict[i] = 'Shelf {}'.format(i)

test_bin_dict = {}
for i in range(1, 27):
    test_bin_dict[i] = 'CD' + str(i)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/items', methods=['GET', 'POST'])
def items():
    form = ItemForm()
    item_list = Item.query.all()
    if request.method == 'GET':
        return render_template('items.html', form=form, items=items)
    else:
        if form.validate():
            new_item = Item(form.sku.data, form.title.data)
            session.add(new_item)
            session.commit()
            form.sku.data = ''
            form.title.data = ''
            return render_template('items.html', form=form, item_list=item_list, item_added=True)
        else:
            return render_template('items.html', form=form, item_list=item_list, item_added=False)


@app.route('/shelves', methods=['GET', 'POST'])
def shelves():
    form = ShelfForm()
    if request.method == 'GET':
        return render_template('shelves.html', form=form, test_shelf_dict=test_shelf_dict)
    else:
        if form.validate():
            test_shelf_dict[form.name.data] = form.name.data
            form.name.data = ''
            return render_template('shelves.html', form=form, test_shelf_dict=test_shelf_dict, shelf_added=True)
        else:
            return render_template('shelves.html', form=form, test_shelf_dict=test_shelf_dict, shelf_added=False)


@app.route('/bins', methods=['GET', 'POST'])
def bins():
    form = BinForm()
    if request.method == 'GET':
        return render_template('bins.html', form=form, test_bin_dict=test_bin_dict)
    else:
        if form.validate():
            test_bin_dict[len(test_bin_dict) + 1] = form.name.data
            form.name.data = ''
            form.shelf_name = ''
            return render_template('bins.html', form=form, test_bin_dict=test_shelf_dict, shelf_added=True)
        else:
            return render_template('bins.html', form=form, test_bin_dict=test_shelf_dict, shelf_added=False)


if __name__ == '__main__':
    app.run()