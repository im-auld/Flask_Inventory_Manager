from flask import Flask, render_template, request
from forms import *


app = Flask(__name__)
app.secret_key = 'secret_shhhhh'
app.debug = True  # TODO: IMPORTANT >> Remove this before pushing live!!!!!!

test_item_dict = {}
for i in range(100, 201):
    test_item_dict['SKU-{}'.format(i)] = 'Thing {}'.format(i)

test_shelf_dict = {}
for i in range(1, 21):
    test_shelf_dict[i] = 'Shelf {}'.format(i)

test_bin_dict = {}
for i in range(1, 27):
    test_bin_dict[i] = 'CD' + str(i)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/items', methods=['GET', 'POST'])
def items():
    form = ItemForm()
    if request.method == 'GET':
        return render_template('items.html', form=form, test_item_dict=test_item_dict)
    else:
        if form.validate():
            test_item_dict[form.sku.data.upper()] = form.title.data
            form.sku.data = ''
            form.title.data = ''
            return render_template('items.html', form=form, test_item_dict=test_item_dict, item_added=True)
        else:
            return render_template('items.html', form=form, test_item_dict=test_item_dict, item_added=False)


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