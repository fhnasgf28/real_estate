from odoo import models, fields, api, _
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
import webbrowser
from urllib.parse import quote


class Estate(models.Model):
    _name = 'estate.property'
    _description = 'Real estate property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string='Title', required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    postcode = fields.Char(string='Postcode', required=True, default='12345', copy=False)
    date_availability = fields.Date(string='Date Availability', readonly=True,
                                    default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(string='Expected price', required=True)
    selling_price = fields.Float(string='Selling price')
    bedroom = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')  # compute & garden area
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')  # , inverse='_inverse_onchange_garden'
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[
        ('N', 'North'),
        ('S', 'South'),
        ('E', 'East'),
        ('W', 'West'),
    ],
                                          help='Orientation of the garden on the property')  # , inverse='_inverse_onchange_garden' , compute='_onchange_garden'
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string='State', default='new', required=True, copy=False)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False, readonly=True)
    salesperson_id = fields.Many2one('res.users', string='Sales Person', default=lambda self: self.env.user.id)
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
    phone = fields.Char(string="Phone", default=62)
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    html_desc = fields.Html(string="Masukan data HTML")

    #report
    #report
    def get_excel_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/estate/estate_report_excel/%s' % self.id,
            'target': 'new',
        }

    def send_to_whatsapp(self):
        if not self.phone:
            raise ValidationError(_("Missing Phone number in patient record"))
        message = 'Hi %s, your postcode number is: %s, Thank You' % (self.name, self.postcode)
        whatsapp_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.phone, message)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_url
        }

        # print('tombol di klik')
        # mobile_number = self.phone
        # message1 = 'Nomor Telepon tidak tersedia untuk record ini, tambahkan nomor telepon terlebih dahulu'
        # if not mobile_number:
        #     return {
        #             'type': 'ir.actions.act_warn',
        #             'title': 'Nomor Telepon Tidak Tersedia',
        #             'message': message1,
        #     }
        #
        # message = 'Halo, saya ingin melakukan pemesanan untuk produk ini'
        #
        # encode_message = quote(message)
        # whatsapp_url = f'https://wa.me/{mobile_number}?text={encode_message}'
        #
        # webbrowser.open(whatsapp_url)
        # return True

    # chapter 9
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area
            print(property.total_area)

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
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
            record.button_state = 'canceled'

    def action_sold(self):
        for record in self:
            if record.button_state == 'canceled':
                raise UserError('A canceled property cannot be set as sold')
            record.button_state = 'sold'
            record.write({'state': 'sold'})

    def action_draft(self):
        for rec in self:
            if rec.button_state == "sold":
                raise UserError("A sold property cannot be set to Draft")
            rec.button_state = 'draft'

    # Chapter 11
    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price >= 0)', 'Expected price must be strictly positive'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling price must be be positive')
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for line in self:
            min_price = 0.9 * line.expected_price
            if not float_is_zero(line.expected_price, precision_digits=2) and float_compare(min_price,
                                                                                            line.selling_price,
                                                                                            precision_digits=2) == 1:
                raise ValidationError(_("Selling price should be 90% of expeceted price"))
            # masih kurang paham

    # ++++++++++++++ chapter 13++++++++++++++++++
    @api.model
    def create(self, values):
        return super(Estate, self).create(values)

    # write
    def write(self, values):
        return super(Estate, self).write(values)

    # ondelete

    def unlink(self):
        properties_to_delete = self.filtered(lambda prop: prop.state not in ['new', 'canceled'])
        if properties_to_delete:
            raise ValidationError('You cannot delete properties with states other than "New" or "Canceled"')
        return super(Estate, self).unlink()
