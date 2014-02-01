#Author: Ian Auld
#Date: '1/15/14'
#PyVer: 2.7
#Title: 'Flask_Inventory_Manager'
#Description:

from flask.ext.wtf import Form
from wtforms.fields import TextField, SubmitField, SelectField, IntegerField
import wtforms


class ItemForm(Form):
    sku = TextField('SKU', [wtforms.validators.Required('A SKU is required.')])
    title = TextField('Title', [wtforms.validators.Required('A title is required.')])
    submit = SubmitField('Submit')


class ShelfForm(Form):
    name = TextField('Name', [wtforms.validators.Required('A Name is required')])
    submit = SubmitField('Submit')


class BinForm(Form):
    name = TextField('Name', [wtforms.validators.Required('A name is required')])
    shelf_name = TextField('Shelf', [wtforms.validators.Required('A bin must be placed on a shelf')])
    submit = SubmitField('Submit')


class SearchForm(Form):
    search_on = SelectField('', choices=[('sku', 'sku'), ('title', 'title')])
    search_term = TextField('Search', [wtforms.validators.Required('Please enter a search term')])
    submit = SubmitField('Submit')
    
class StockForm(Form):
    in_out = SelectField('', choices=[('in', 'move item in'),('out', 'move item out')])
    item = TextField('Item', [wtforms.validators.Required('Item is required')])
    bin = TextField('Bin', [wtforms.validators.Required('Bin is required')])
    qty = IntegerField('QTY', [wtforms.validators.Required('QTY is required')])
    submit = SubmitField('Add')