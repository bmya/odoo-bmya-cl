from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    purchase_order_not_add_lines = fields.Boolean(
        default=True, string='Do not add purchase order lines', help='If checked, this allows to check if the selected'
        ' PO lines match with some of the invoice lines, and establish the relationship between them.')
    purchase_order_match = fields.Boolean(compute='_check_purchase_order_match', default=False)
    purchase_order_price_match = fields.Boolean(compute='_check_purchase_order_match', default=False)
    purchase_order_full_match = fields.Boolean(compute='_check_purchase_order_match', default=False)
    purchase_order_products_received = fields.Boolean(
        compute='_check_purchase_order_match', string='Products received', default=False)
    purchase_order_line_all_products_received = fields.Boolean(
        compute='_check_purchase_order_match', string='All Products Received', default=False)
    purchase_order_invoice_lines_match = fields.Boolean(
        compute='_check_purchase_order_match', string='All PO Match', default=False)

    def check_match(self):
        for record in self:
            # criteria # 1: there is something in the field invoice_origin that matches a purchase order,
            # otherwise show a warning alert
            record.purchase_order_match = record.invoice_origin
            po_obj = self.env['purchase.order'].search([['name', '=', record.invoice_origin]])
            record.purchase_order_full_match = (record.amount_untaxed == po_obj.amount_untaxed)
            purchase_order_products_received = False
            purchase_order_price_match = False
            purchase_order_line_all_products_received = False
            # po_list = record.line_ids.filtered(lambda s: s.purchase_line_id).mapped('purchase_line_id')
            # move_ids = self.env['account.move.line'].search([['purchase_line_id', 'in', po_list.ids]])
            for line in record.line_ids.filtered(lambda s: s.purchase_line_id):
                # criteria # 2: the total untaxed of the referred origin order, matches the total of the invoice,
                # otherwise show a warning alert
                if line.purchase_line_id.qty_invoiced <= line.purchase_line_id.qty_received:
                    purchase_order_products_received |= True
                ##  else:
                ##      purchase_order_products_received &= False
                # criteria # 3: the products in the invoice, has been received (they are in quantity received,
                # tracked in the purchase order. Otherwise show a warning alert
                # (disregarding the criteria configured in Odoo)
                if line.purchase_line_id.qty_invoiced == line.purchase_line_id.qty_received:
                    purchase_order_line_all_products_received |= True
                ##  else:
                ##      purchase_order_line_all_products_received &= False
                # criteria # 4: the unit price of the product invoices is equal to the unit price of the PO
                # otherwise, show a danger alert
                if line.price_unit == line.purchase_line_id.price_unit:
                    purchase_order_price_match |= True
            record.purchase_order_products_received = purchase_order_products_received
            record.purchase_order_price_match = purchase_order_price_match
            record.purchase_order_line_all_products_received = purchase_order_line_all_products_received
            # criteria # 5: if sum of items received (tracked in PO) matches sum of items in the invoice,
            # show a success alert.
            # criteria # 6: if besides criteria # 5: the amount of the invoice equals the order, show a second
            # success alert.
            record.purchase_order_invoice_lines_match = (
                    sum(record.line_ids.filtered(lambda s: s.purchase_line_id).mapped('quantity')) == sum(
                po_obj.order_line.mapped('qty_received')))
            # criteria # 7: additionally, if there is a reception linked to the PO or the invoice, show another
            # set of alerts (todo...)
            # criteria # 8: l10n-cl: Integrates to the on-changes, referenced documents (todo...)

    def match_purchase_order(self, purchase_id):
        self.fiscal_position_id = purchase_id.fiscal_position_id if not self.fiscal_position_id else \
            self.fiscal_position_id
        self.invoice_payment_term_id = purchase_id.payment_term_id
        self.currency_id = purchase_id.currency_id if not self.currency_id else self.currency_id
        invoice_lines = self.line_ids.filtered(lambda s: not s.purchase_line_id)
        po_lines = purchase_id.order_line - self.line_ids.filtered(lambda s: s.purchase_line_id).mapped(
            'purchase_line_id')
        for line in po_lines:
            il = invoice_lines.filtered(lambda s: s.product_id == line.product_id)
            if il:
                il.purchase_line_id = line.id
        # Compute invoice_origin.
        origins = set(self.line_ids.mapped('purchase_line_id.order_id.name'))
        self.invoice_origin = ','.join(list(origins))
        # Compute ref.
        refs = set(self.line_ids.mapped('purchase_line_id.order_id.partner_ref'))
        refs = [ref for ref in refs if ref]
        self.ref = ','.join(refs)
        # Compute invoice_payment_ref.
        if len(refs) == 1:
            self.invoice_payment_ref = refs[0]
        self._onchange_currency()
        self.invoice_partner_bank_id = self.bank_partner_id.bank_ids and self.bank_partner_id.bank_ids[0]

    @api.depends('line_ids', 'invoice_origin')
    def _check_purchase_order_match(self):
        for record in self:
            record.check_match()

    @api.onchange('purchase_vendor_bill_id', 'purchase_id')
    def _onchange_purchase_auto_complete(self):
        # this boolean allows to override the default Odoo behaviour if not set
        if not self.purchase_order_not_add_lines:
            return super()._onchange_purchase_auto_complete()
        # otherwise, make all the matches without replicating the PO lines
        if self.purchase_vendor_bill_id.vendor_bill_id:
            self.invoice_vendor_bill_id = self.purchase_vendor_bill_id.vendor_bill_id
            self._onchange_invoice_vendor_bill()
        elif self.purchase_vendor_bill_id.purchase_order_id:
            self.purchase_id = self.purchase_vendor_bill_id.purchase_order_id
        self.purchase_vendor_bill_id = False
        if not self.purchase_id:
            return
        self.match_purchase_order(self.purchase_id)
        self.purchase_id = False
