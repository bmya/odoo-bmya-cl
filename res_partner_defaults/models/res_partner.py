# -*- coding: utf-8 -*-
from openerp import fields, models


class res_partner(models.Model):
    _inherit = 'res.partner'

    def _default_partner_type(self):
        return True

    is_company = fields.Boolean('Is Company', default=_default_partner_type)
