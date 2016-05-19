# -*- coding: utf-8 -*-
{
    'name': 'Chilean VAT Ledger',
    'license': 'AGPL-3',
    'description': '''
Chilean VAT Ledger Management
=================================
Creates Sale and Purchase VAT report menus in
"accounting/period processing/VAT Ledger"
    ''',
    'version': '0.3',
    'author': u'Blanco Martín & Asociados',
    'website': 'http://blancomartin.cl',
    'depends': [
        'report_aeroo',
        'l10n_cl_invoice'
    ],
    'category': 'Reporting subsystems',
    'data': [
        'account_vat_report_view.xml',
        'report/account_vat_ledger_report.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'active': False
}
