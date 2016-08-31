# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  Blanco Martin & Asociados  (http://blancomartin.cl)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": """Chile - Web Services de Documentos Tributarios Electrónicos\
    """,
    'version': '8.0.2.0.0',
    'category': 'Localization/Chile',
    'sequence': 12,
    'author':  'Blanco Martín & Asociados',
    'website': 'http://blancomartin.cl',
    'license': 'AGPL-3',
    'summary': '',
    'description': """
Chile: API and GUI to access Electronic Invoicing webservices.
""",
    'depends': [
        'webservices_generic',
        'l10n_cl_counties',
        'l10n_cl_invoice',
        ],
    'external_dependencies': {
        'python': [
            'xmltodict',
            'dicttoxml',
            'base64',
            'cchardet',
            'urllib3',
        ]
    },
    'data': [
        'views/invoice_view.xml',
        'views/partner_view.xml',
        'views/company_view.xml',
        'views/payment_t_view.xml',
        'views/sii_regional_offices_view.xml',
        'views/invoice_template.xml',
        'data/sii.regional.offices.csv',
        'security/ir.model.access.csv',
        'wizard/dte_status_update_view.xml',
        'wizard/account_invoice_refund_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
