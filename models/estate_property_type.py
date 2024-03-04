from odoo import models, fields, api
from datetime import date, timedelta


class Estate(models.Model):
    _name = 'estate.property.type'
    _description = 'Real estate property type'


    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    # tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    # price = fields.Float(string='Price')
    # status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', default='accepted',
    #                           copy=False)
    # date_deadline = fields.Date(string='Deadline')
    # partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    # property_id1 = fields.Many2one('estate.property', string='Property', required=True)


