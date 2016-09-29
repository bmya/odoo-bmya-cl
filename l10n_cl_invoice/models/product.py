# -*- coding: utf-8 -*-
from openerp import fields, models, api


class productTemplate(models.Model):
    _inherit = 'product.template'

    # Esto no sé que es... estaba hecho, pero estaba sin aplicar
    # porque no llamaba al código este desde el __init__
    # type = fields.Selection(
    #     [('adjust', 'Adjust concept'),
    #      ('consu', 'Consumable'),
    #      ('service', 'Service')], 'Product Type', required=True,
    #         help="Adjust concept are items to be incremented in the client \
    #         account by invoice errors, interest or other reasons, consumable \
    #         are product where you don't manage stock, a service is a \
    #         non-material product provided by a company or an individual.")]

    # TODO: mejorar la vista, de tal manera que si el producto es exento los
    # impuestos no los permita editar
    # TODO: cambiar la vista, para que los impuestos no se puedan poner en la
    # linea del producto
    # por ahora, l10n_cl_dte busca los asserts que permitan validar que lo que
    # se hace está bien.
    is_exempt = fields.Boolean('Sales Tax Exempt', default=False)

    @api.onchange('is_exempt')
    def _reset_tax(self):
        if self.is_exempt:
            self.taxes_id = False


class productProduct(models.Model):
    _inherit = 'product.product'

    is_exempt = fields.Boolean(
        'Sales Tax Exempt', default=False,
        related='product_tmpl_id.is_exempt')

    @api.onchange('is_exempt')
    def _reset_tax(self):
        if self.is_exempt:
            self.taxes_id = False
