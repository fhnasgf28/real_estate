from odoo import models, fields, api

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real estate property tag'

    name = fields.Char(string='Title', required=True)


    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)', 'Property tag names must be unique')
    ]