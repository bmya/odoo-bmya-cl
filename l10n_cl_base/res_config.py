# -*- coding: utf-8 -*-
# Init module for l10n_cl_base
# Daniel Blanco - Blanco Martin & Asociados
##############################################################################
'''This code intended to define transient fields for installing modules'''
from openerp import models, fields, api

# TODO: para que no falle el tipo de contribuyente (tax payer type) en una
# empresa que ya está funcionando, el wizard debe preguntar la compañia y pedir
# que se fije el tipo de contribuyente acá mismo, para evitar comflictos.
# mientras se desactiva ese código en la compañia. (l10n_cl_invoice)

class chilean_base_configuration(models.TransientModel):
    '''Inherit Odoo base config'''
    _name = 'chilean.base.config.settings'
    _inherit = 'res.config.settings'

    module_l10n_cl_chart = fields.Boolean(
        'Install Chilean Accounting Plan',
        help="""Installs module l10n_cl_chart, allowing to choose different \
account options.""")

    module_l10n_cl_account_vat_ledger = fields.Boolean(
        'Install VAT Ledger',
        help="""Installs module l10n_cl_account_vat_ledger, allowing to export \
sales and purchases VAT ledger in XLS format. Requires Aeroo Reports.""")

    module_l10n_cl_banks_sbif = fields.Boolean(
        'Banks in Chile, According SBIF',
        help="""Installs module l10n_cl_banks_sbif, and includes authorized \
banks, and financial institutions in Chile.""")

    module_account_bank_voucher = fields.Boolean(
        'Reconcile payments directly importing vouchers to account bank \
statement', help="""Installs account_bank_voucher, allowing you to reconcile \
payments to/from partners directly in bank statement.""")

    module_l10n_cl_financial_indicators = fields.Boolean(
        'Update UF, UTM, Dollar and Euro automatically',
        help="""Installs module l10n_cl_financial_indicators, allowing to \
update indicators daily, from SBIF.""")

    module_l10n_cl_counties = fields.Boolean(
        'Include Chilean Counties for partners and companies',
        help="""Installs l10n_cl_counties, which includes all chilean \
counties to partners.""")

    module_l10n_cl_partner_activities = fields.Boolean(
        'Include Partner\'s turn', help="""Installs l10n_cl_partner_activities \
module, which includes your partners' turns in their record using the SII \
activities table and allows you to select the activity when invoicing.""")

    module_l10n_cl_invoice = fields.Boolean(
        'Centralized sales journal for multiple type of document stubs \
         (recommended)!',
        help="""Installs l10n_cl_invoice. It links your invoicing, picking and \
receipts stubs with journals for easiest configuration. This is a base module \
for DTE compliance, and a fundamental option for companies with multiple \
branches.""")

    module_l10n_cl_dte = fields.Boolean(
        'Use Electronic Invoicing', help="""Installs several dependencies in \
order to performn Electronic invoicing, and sales invoicing in xml.""")

    module_user_signature_key = fields.Boolean(
        'SII Directly (adds User signature and CAF management).',
        help="""Works without gateways, directly to SII. This set Odoo to \
work directly with SII, installing module l10n_cl_dte_caf and \
other dependencies""")

    module_l10n_cl_pos_basic_users = fields.Boolean(
        'Install dummy-proof terminology - (not recommended)',
        help="""Installs l10n_cl_pos_basic_users module, which helps \
against POS closed minded operators. (factura/boleta cliente factura, \
cliente boleta. Adds generic partners to make invoicing easier, but is not \
recommended, except for dummy users.""")

    module_l10n_cl_pos_credit_card_voucher = fields.Boolean(
        'Exclude final consumer credit card sales from VAT report (recommended \
only for pre-printed invoicing)',
        help="""Installs module l10n_cl_pos_credit_card_voucher, allowing you \
to link the sales note with a credit card voucher, in order to keep \
it unreported in boletas sales.""")

    module_invoice_printed = fields.Boolean(
        'Invoice in TXT Format', help="""Installs invoice_printed module, to \
interact with prnfiscal dependency in your local machine, in order to have \
your fiscal documents rendered in TXT format. This allows printing in fiscal \
printers, or connect to external electronic invoices services""")

    module_l10n_cl_aeroo_einvoice = fields.Boolean(
        'Electronic Invoice Format', help="""Installs output form report \
including PDF417 electronic stamp""")

    module_l10n_cl_dte_pdf = fields.Boolean(
        'Electronic Invoice Format', help="""Installs output form report \
    including PDF417 electronic stamp""")

    module_l10n_cl_aeroo_stock = fields.Boolean(
        'Electronic Stock picking', help="""Installs output form report \
including PDF417 electronic stamp""")

    module_l10n_cl_aeroo_purchase = fields.Boolean(
        'Purchase Order Form', help="""Report for purchase order""")

    module_l10n_cl_aeroo_sale = fields.Boolean(
        'Sales Order Form', help="""Report for sales order""")

    module_l10n_cl_aeroo_receipt = fields.Boolean(
        'Payment Receipt Form', help="""Report for payment receipt""")

    module_l10n_cl_hr_payroll = fields.Boolean(
        'Install payroll and AFPs chilean modules',
        help="""Install l10n_cl_hr_payroll for payroll and AFPs chilean \
modules""")

    module_l10n_cl_hr_previred = fields.Boolean(
        'Update Previred\'s Monthly indexes',
        help="""Installs l10n_cl_hr_previred module, to update needed indexes \
in order to issue your payroll""")

    module_l10n_cl_hr_send_to_previred = fields.Boolean(
        'Send payroll Information to Previred monthly',
        help="""Installs l10n_cl_send_to_previred module, which allows you to \
send a monthly report with 105 fields per employee, to Previred.""")


    module_l10n_cl_base_rut = fields.Boolean(
        'Validate Chilean VAT (RUT) and format to 99.999.999-X',
        help="""Installs l10n_cl_base_rut in ordar to validate de VAT (RUT) \
        ant to have it formatted correctly, according Chilean usage.""")

    @api.onchange('module_l10n_cl_invoice') # if these fields are changed, call method
    def check_change_cl_invoice(self):
        if self.module_l10n_cl_invoice == True:
            self.module_l10n_cl_partner_activities = True
            self.module_l10n_cl_base_rut = True

    @api.onchange('module_l10n_cl_dte', 'module_l10n_cl_account_vat_ledger')  # if these fields are changed, call method
    def check_change_cl_dte(self):
        if self.module_l10n_cl_dte == True or self.module_l10n_cl_account_vat_ledger == True:
            self.module_l10n_cl_invoice = True
            self.module_l10n_cl_counties = True

