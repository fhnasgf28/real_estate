from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError
class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real estate property offer'
    _order = 'price desc'

    price = fields.Float(string='Price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', default='accepted',)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    # for stat button
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', related='property_id.property_type_id', store=True)
    validity = fields.Integer('Validity (days)', default=7)
    create_date = fields.Datetime(string='Create Date')
    is_offer_accepted = fields.Boolean(compute="_is_offer_accepted")

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

    @api.model
    def create(self, vals):
        property_obj = self.env['estate.property'].browse(vals.get("property_id"))
        existing_offers = property_obj.offer_ids.filtered(lambda offer: offer.price >= vals.get('price'))
        if existing_offers:
            raise ValidationError("You Cannot create an offer with a lower amount than an existing offer")

    #     menetapkan status property menjadi 'offer Received'
        property_obj.state = 'offer_received'

        return super(EstatePropertyOffer, self).create(vals)

    # chapter 11
    # _sql_constraints = [
    #     ('check_price_positive', 'CHECK(price > 0)', 'Offer Price must be strictly positive.')
    # ]

    def action_accept_offer(self):
        for offer in self:
            offer.write({'status': 'accepted'})
            offer.property_id.selling_price = offer.property_id.best_price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.write({'state': 'offer_accepted'})
    @api.depends('property_id.state')
    def _is_offer_accepted(self):
        for record in self:
            record.is_offer_accepted = record.property_id.state == 'offer_accepted'

    def action_refused(self):
        for offer in self:
            offer.status = 'refused'

    # chapter 11
    @api.constrains('price')
    def _price_not_nol(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("Offer Price must be strictly positive.")


    # def action_accepted(self):
    #     for offer in self:
    #         offer.write({'status': 'accepted'})
    #         offer.property_id.selling_price = offer.property_id.best_price
    #         offer.property_id.buyer_id = offer.partner_id
    #         offer.property_id.write({'state': 'offer_accepted'})
    #
    # def action_refused(self):
    #     for offer in self:
    #         offer.write({'status': 'refused'})

    # for offer in self:
    #     best_price = self.env['estate.property.offer'].search(
    #         [('property_id', '=', offer.property_id.id), ('status', '=', 'accepted')], order='price desc', limit=1)
    #     if best_price:
    #         offer.property_id.write({'selling_price': best_price.price, 'buyer_id': best_price.partner_id.id})
    #     offer.write({'status': 'accepted'})
