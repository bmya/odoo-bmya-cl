# -*- coding: utf-8 -*-
# Init module for l10n_cl_base
# Daniel Blanco - Blanco Martin & Asociados
##############################################################################
'''This code intended to define transient fields for installing modules'''
from odoo import models, fields


class chilean_base_configuration(models.TransientModel):
    '''Inherit Odoo base config'''
    _name = 'chilean.base.config.settings'
    _inherit = 'res.config.settings'

    module_l10n_cl_banks_sbif = fields.Boolean(
        'Banks in Chile, According SBIF',
        help="""Installs module l10n_cl_banks_sbif, and includes authorized
banks, and financial institutions in Chile.""")

    module_l10n_cl_chart = fields.Boolean(
        'Install Chilean Accounting Plan',
        help="""Installs module l10n_cl_chart, allowing to
choose different account options.""")

    module_l10n_cl_financial_indicators = fields.Boolean(
        'Update UF, UTM, Dollar and Euro automatically',
        help="""Installs module l10n_cl_financial_indicators, allowing to
update indicators daily, from SBIF.""")

    module_l10n_cl_account_vat_ledger = fields.Boolean(
        'Install VAT Ledger',
        help="""Installs module l10n_cl_account_vat_ledger, allowing to
export sales and purchases VAT ledger in XLS format. Requires Aeroo Reports.""")

    module_account_bank_voucher = fields.Boolean(
        'Reconcile payments directly importing vouchers to account bank statement',
        help="""Installs account_bank_voucher, allowing you to reconcile payments
to/from partners directly in bank statement.""")

    module_l10n_cl_invoice = fields.Boolean(
        'Allows to have your stubs presented to the same sales journal',
        help="""Installs l10n_cl_invoice Link your invoicing, picking and
receipts stubs with journals for easiest configuration.""")

    module_l10n_cl_credit_card_voucher = fields.Boolean(
        'Exclude your final consumer credit card sales from VAT report',
        help="""Installs module l10n_cl_credit_card_voucher, allowing you
to link the sales note with a credit card voucher, in order to keep
it unreported in boletas sales.""")

    module_l10n_cl_wssii_fe = fields.Boolean(
        'Use Electronic Invoicing', help="""Installs several dependencies in
order to performn Electronic invoicing, sales reports in xml, and """)

    module_invoice_printed = fields.Boolean(
        'Invoice in TXT Format', help="""Installs invoice_printed module, to
interact with prnfiscal dependency in your local machine, in order to have your
fiscal documents rendered in TXT format. This allows printing in fiscal
printers, or connect to external electronic invoices services""")

    module_l10n_cl_aeroo_einvoice = fields.Boolean(
        'Electronic Invoice Format', help="""Installs output form report
including PDF417 electronic stamp""")

    module_l10n_cl_aeroo_stock = fields.Boolean(
        'Electronic Stock picking', help="""Installs output form report
including PDF417 electronic stamp""")

    module_l10n_cl_aeroo_purchase = fields.Boolean(
        'Purchase Order Form', help="""Report for purchase order""")

    module_l10n_cl_aeroo_sale = fields.Boolean(
        'Sales Order Form', help="""Report for sales order""")

    module_l10n_cl_aeroo_receipt = fields.Boolean(
        'Payment Receipt Form', help="""Report for payment receipt""")

    module_l10n_cl_partner_activities = fields.Boolean(
        'Include Partner\'s turn', help="""Installs l10n_cl_partner_activities
module, which includes your partners' turns in their record using the SII
activities table and allows you to select the activity when invoicing.""")

    module_l10n_cl_hr_payroll = fields.Boolean(
        'Install payroll and AFPs chilean modules',
        help="""Install l10n_cl_hr_payroll for payroll and AFPs chilean
modules""")

    module_l10n_cl_hr_previred = fields.Boolean(
        'Update Previred\'s Monthly indexes',
        help="""Installs l10n_cl_hr_previred module, to update needed indexes
in order to issue your payroll""")

    module_l10n_cl_hr_send_to_previred = fields.Boolean(
        'Send payroll Information to Previred monthly',
        help="""Installs l10n_cl_send_to_previred module, which allows you to
send a monthly report with 105 fields per employee, to Previred.""")

    module_l10n_cl_fantasy_name = fields.Boolean(
        'Add Fantasy Name to Partners',
        help="""Add a fields to your partners with their fantasy name, and
allows you to search them by this name.""")

    module_l10n_cl_toponyms = fields.Boolean(
        'Include Chilean Counties', help="""Installs l10n_cl_toponyms, which
includes all chilean counties to partners.""")

    module_l10n_cl_base_rut = fields.Boolean(
        'Validate Chilean VAT (RUT) and format to 99.999.999-X',
        help="""Installs l10n_cl_base_rut in ordar to validate de VAT (RUT) \
        ant to have it formatted correctly, according Chilean usage.""")

