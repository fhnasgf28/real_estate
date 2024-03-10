from odoo import models, fields, api
from datetime import timedelta
class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real estate property offer'

    price = fields.Float(string='Price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', default='accepted', copy=False, accepted='accepted', refused='refused')
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    create_date = fields.Datetime(string='Create Date')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer.create_date + timedelta(
                days=offer.validity) if offer.create_date else fields.Date.today() + timedelta(days=offer.validity)

    @api.depends('date_deadline')
    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                offer_create_date = offer.create_date.date()
                offer.validity = (offer.date_deadline - offer_create_date).days
            else:
                offer.validity = 7

    # chapter 11
    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)', 'Offer Price must be strictly positive.')
    ]

    def action_accept_offer(self):
        for offer in self:
            offer.button_state = 'accepted'

    def action_refuse_offer(self):
        for offer in self:
            offer.button_state = 'refused'