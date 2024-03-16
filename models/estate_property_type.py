from odoo import models, fields, api
from datetime import date, timedelta


class Estate(models.Model):
    _name = 'estate.property.type'
    _description = 'Real estate property type'
    _order = 'name'


    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence', default=1, help='Used to order stages. Lower is better')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string='Offer Count', compute='_compute_offer_count')

    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'Property type names must be unique.')
    ]

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    # price = fields.Float(string='Price')
    # status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', default='accepted',
    #                           copy=False)
    # date_deadline = fields.Date(string='Deadline')
    # partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    # property_id1 = fields.Many2one('estate.property', string='Property', required=True)


