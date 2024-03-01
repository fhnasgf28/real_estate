from odoo import models, fields, api
from datetime import date, timedelta


class Estate(models.Model):
    _name = 'estate.property.type'
    _description = 'Real estate property type'


    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')



