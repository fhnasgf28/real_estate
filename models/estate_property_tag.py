from odoo import models, fields, api

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real estate property tag'

    name = fields.Char(string='Title', required=True)
