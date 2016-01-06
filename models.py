# -*- coding: utf-8 -*-
from openerp import models, fields


class account_invoice(models.Model):
    _inherit = "account.invoice"

    ccvoucher_line_ids = fields.One2many('account.invoice.ccvoucher', 'invoice_id', string='Credit Card Voucher Lines',
                                     states={'draft': [('readonly', False)]}, readonly=True, copy=True)


class account_journal(models.Model):
    _inherit = "account.journal"

    add_credit_card_voucher_number = fields.Boolean("Add credit card voucher number", default=False)


class account_invoice_ccvoucher(models.Model):
    _name = "account.invoice.ccvoucher"
    _description = "Credit Card Voucher"

    invoice_id = fields.Many2one('account.invoice', string='Invoice Line', ondelete='cascade', index=True)
    voucher_number = fields.Char('Credit Card Voucher Number')


class pos_order_ccvoucher(models.Model):
    _name = "pos.order.ccvoucher"

    order_id = fields.Many2one('pos.order', 'order_id', ondelete='cascade', index=True)
    voucher_number = fields.Char('Credit Card Voucher Number')


class pos_order(models.Model):
    _inherit = "pos.order"

    ccvoucher_order_ids = fields.One2many('pos.order.ccvoucher', 'order_id', copy=True)

    def _process_order(self, cr, uid, order, context=None):
        order_id = super(pos_order, self)._process_order(cr, uid, order, context)
        for paymentline in order['statement_ids']:
            self.pool.get('pos.order.ccvoucher').create(cr, uid, {'order_id': order_id,
                                                                  'voucher_number': paymentline[2]['ccvoucher']
                                                                  })
        return order_id

    def action_invoice(self, cr, uid, ids, context=None):
        res = super(pos_order, self).action_invoice(cr, uid, ids, context)

        inv_voucher_ref = self.pool.get('account.invoice.ccvoucher')
        for order in self.pool.get('pos.order').browse(cr, uid, ids, context=context):
            invoice_id = self.pool.get('account.invoice').search(cr, uid, [('origin', '=', order.name)], context=context)
            for line in order.ccvoucher_order_ids:
                inv_voucher_ref.create(cr, uid, {'invoice_id': invoice_id[0],
                                                 'voucher_number': line.voucher_number,
                                                 }, context=context)
        return res
