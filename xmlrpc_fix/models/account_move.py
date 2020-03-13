# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    def post(self):
        super().post()
        return True
