from odoo import models, fields, api


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real estate property tag'
    _order = 'name'

    name = fields.Char(string='Title', required=True)
    color = fields.Integer(string='color Tag')
    active = fields.Boolean(string="Boolean", default=True)

    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)', 'Property tag names must be unique')
    ]
