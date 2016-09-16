# -*- coding: utf-8 -*-
from openerp import fields, models


class product_template(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(
        [('adjust', 'Adjust concept'),
         ('consu', 'Consumable'),
         ('service', 'Service')], 'Product Type', required=True,
            help="Adjust concept are items to be incremented in the client \
            account by invoice errors, interest or other reasons, consumable \
            are product where you don't manage stock, a service is a \
            non-material product provided by a company or an individual.")]
    is_excempt = fields.Boolean('Excempt Product', default=False)

    @api.onchange('is_excempt')
    def _reset_tax(self):
        pass



