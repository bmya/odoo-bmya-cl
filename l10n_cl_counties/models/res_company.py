from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    city_id = fields.Many2one("res.city", related='partner_id.city_id', string='Comuna')
    country_id = fields.Many2one("res.country", related='partner_id.country_id', string='Country',
                                 default=lambda self: self.env.ref('base.cl'))
    state_id = fields.Many2one("res.country.state", related='partner_id.state_id', string='Ubication',
        domain="[('country_id', '=', country_id), ('type', '=', 'normal'), ('id', '!=', id)]", readonly=True)
    real_city = fields.Char(related='partner_id.real_city', string='City')

    # @api.onchange('city_id', 'city', 'state_id')
    # def _change_city_province(self):
    #     if self.country_id != self.env.ref('base.cl'):
    #         return
    #     self.state_id = self.city_id.state_id.parent_id
    #     if self.state_id == self.env.ref('base.state_cl_13'):
    #         self.city = 'Santiago'
    #     else:
    #         self.city = self.city_id.name
