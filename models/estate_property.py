from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import UserError


class Estate(models.Model):
    _name = 'estate.property'
    _description = 'Real estate property'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode', required=True, default='12345', copy=False)
    date_availability = fields.Date(string='Date Availability', readonly=True,
                                    default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(string='Expected price', required=True)
    selling_price = fields.Float(string='Selling price', readonly=True)
    bedroom = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area', compute='_onchange_garden', inverse='_inverse_onchange_garden')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[
        ('N', 'North'),
        ('S', 'South'),
        ('E', 'East'),
        ('W', 'West'),
    ], help='Orientation of the garden on the property', compute='_onchange_garden', inverse='_inverse_onchange_garden')
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer received', 'Offer Received'),
        ('offer accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string='State', default='new', required=True, copy=False)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Sales Person', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')  # inverse
    # size = fields.Char(related='property_type_id.size')
    total_area = fields.Float('Total Area', compute='_compute_total_area')
    best_price = fields.Float('Best Offer', compute='_compute_best_price')
    # Chapteer 10
    button_state = fields.Selection([
        ('draft', 'Draft'),
        ('canceled', 'Canceled'),
        ('sold', 'Sold')
    ], default='draft', string='Status', readonly=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'), default=0.0)

    @api.depends('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'N'
            else:
                record.garden_area = False
                record.garden_orientation = False

    @api.depends('garden_area', 'garden_orientation')
    def _inverse_onchange_garden(self):
        for record in self:
            if record.garden_area or record.garden_orientation:
                record.garden = True
            else:
                record.garden = False

    #                 Chapter 10

    def action_cancel(self):
        for record in self:
            if record.button_state == 'sold':
                raise UserError('A sold property cannot be canceled')
            property.button_state = 'canceled'

    def action_sold(self):
        for record in self:
            if record.button_state == 'canceled':
                raise UserError('A canceled property cannot be set as sold')
            record.button_state = 'sold'
