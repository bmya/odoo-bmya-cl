from odoo import fields, models


class ResCity(models.Model):
    _name = 'res.city'
    _inherit = 'res.city'

    code = fields.Char(
        'City Code', size=32, help='The city code.')
    type = fields.Selection(
        [('view', 'View'), ('normal', 'Normal')], 'Type', default='normal')
