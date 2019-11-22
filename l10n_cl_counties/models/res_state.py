from odoo import api, fields, models


class ResState(models.Model):
    _name = 'res.country.state'
    _inherit = 'res.country.state'

    code = fields.Char(
        'State Code', size=32, help='The state code.\n', required=True)
    complete_name = fields.Char(
        string='Complete Name')
    parent_id = fields.Many2one(
        'res.country.state', 'Parent State', index=True,
        domain="[('type', '=', 'view'), ('id', '!=', id)]")
    child_ids = fields.One2many(
        'res.country.state', 'parent_id', string='Child States')
    type = fields.Selection(
        [('view', 'View'), ('normal', 'Normal')], 'Type', default='normal')
