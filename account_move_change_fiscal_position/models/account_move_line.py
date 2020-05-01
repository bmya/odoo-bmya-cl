from odoo import models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('fiscal_position_id')
    def _compute_taxes(self):
        """
        Agregada por Daniel Blanco para recalcular impuestos y cuentas contables al cambiar la posicion fiscal
        """
        for line in self.line_ids:
            line._onchange_product_id()
            line._onchange_debit()
            line._onchange_credit()
        self._recompute_tax_lines()
