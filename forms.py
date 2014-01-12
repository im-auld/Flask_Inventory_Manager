__author__ = 'ian'

from flask.ext.wtf import Form
from wtforms.fields import TextField, SubmitField
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


