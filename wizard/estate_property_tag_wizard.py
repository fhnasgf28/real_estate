from odoo import models, fields, api


class EstatePropertyTag(models.TransientModel):
    _name = 'estate.property.tag.wizard'
    _description = 'Real estate property tag'

    property_tag_id = fields.Many2one('estate.property.tag', string='Property Tag')

    def action_cancel(self):
        print('oke sudah bisa di klik')
        return
