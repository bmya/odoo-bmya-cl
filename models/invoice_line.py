# -*- coding: utf-8 -*-
from openerp import osv, models, fields, api, _
from openerp.osv import fields as old_fields
from openerp.exceptions import except_orm, Warning
import openerp.addons.decimal_precision as dp
# from inspect import currentframe, getframeinfo
# estas 2 lineas son para imprimir el numero de linea del script
# (solo para debug)
# frameinfo = getframeinfo(currentframe())
# print(frameinfo.filename, frameinfo.lineno)


class account_invoice_line(models.Model):

    """
    En Chile como no se discriminan los impuestos en las facturas, excepto el IVA,
    agrego campos que ignoran el iva solamente a la hora de imprimir los valores.
    (excepción: liquidación factura)
    """

    _inherit = "account.invoice.line"

    def _printed_prices(self, cr, uid, ids, name, args, context=None):
        res = {}
        tax_obj = self.pool['account.tax']
        cur_obj = self.pool.get('res.currency')

        for line in self.browse(cr, uid, ids, context=context):
            _round = (lambda x: cur_obj.round(
                cr, uid, line.invoice_id.currency_id, x)) if line.invoice_id else (lambda x: x)
            quantity = line.quantity
            discount = line.discount
            printed_price_unit = line.price_unit
            printed_price_net = line.price_unit * \
                (1 - (discount or 0.0) / 100.0)
            printed_price_subtotal = printed_price_net * quantity

            not_vat_taxes = [
                x for x in line.invoice_line_tax_id if x.tax_code_id.parent_id.name != 'IVA']
            taxes = tax_obj.compute_all(cr, uid,
                                        not_vat_taxes, printed_price_net, 1,
                                        product=line.product_id,
                                        partner=line.invoice_id.partner_id)
            other_taxes_amount = _round(
                taxes['total_included']) - _round(taxes['total'])

            # TODO: tal vez mejorar esto de que se buscan los iva por el que tiene padre llamado "IVA"
            # Antes habiamos agregado un vampo vat_tax en los code pero el tema
            # es que tambien hay que agregarlo en el template de los tax code y
            # en los planes de cuenta, resulta medio engorroso
            # Daniel Blanco: esto me gusta más con el campo "vat tax" en los impuestos
            # queda para arreglarlo.
            vat_taxes = [
                x for x in line.invoice_line_tax_id if x.tax_code_id.parent_id.name == 'IVA']
            taxes = tax_obj.compute_all(cr, uid,
                                        vat_taxes, printed_price_net, 1,
                                        product=line.product_id,
                                        partner=line.invoice_id.partner_id)
            vat_amount = _round(
                taxes['total_included']) - _round(taxes['total'])

            exempt_amount = 0.0
            if not vat_taxes:
                exempt_amount = _round(taxes['total_included'])

            # For document that not discriminate we include the prices
            if not line.invoice_id.vat_discriminated:
                printed_price_unit = _round(
                    taxes['total_included'] * (1 + (discount or 0.0) / 100.0))
                printed_price_net = _round(taxes['total_included'])
                printed_price_subtotal = _round(
                    taxes['total_included'] * quantity)

            res[line.id] = {
                'printed_price_unit': printed_price_unit,
                'printed_price_net': printed_price_net,
                'printed_price_subtotal': printed_price_subtotal,
                'vat_amount': vat_amount * quantity,
                'other_taxes_amount': other_taxes_amount * quantity,
                'exempt_amount': exempt_amount * quantity,
            }
        return res

    _columns = {
        'printed_price_unit': old_fields.function(
            _printed_prices, type='float',
            digits_compute=dp.get_precision('Account'),
            string='Unit Price', multi='printed',),
        'printed_price_net': old_fields.function(
            _printed_prices, type='float',
            digits_compute=dp.get_precision('Account'),
            string='Net Price', multi='printed'),
        'printed_price_subtotal': old_fields.function(
            _printed_prices, type='float',
            digits_compute=dp.get_precision('Account'),
            string='Subtotal', multi='printed'),
        'vat_amount': old_fields.function(
            _printed_prices, type='float',
            digits_compute=dp.get_precision('Account'),
            string='Vat Amount', multi='printed'),
        'other_taxes_amount': old_fields.function(
            _printed_prices, type='float',
            digits_compute=dp.get_precision('Account'),
            string='Other Taxes Amount', multi='printed'),
        'exempt_amount': old_fields.function(
            _printed_prices, type='float',
            digits_compute=dp.get_precision('Account'),
            string='Exempt Amount', multi='printed'),
    }
