# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  BMyA SA / Blanco Martin & Asociados
#    (http://blancomartin.cl)
#    All Rights Reserved.o
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
    'name': 'Account Invoice Partner Commercial',
    'version': '8.0.1.0.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': 'Invoicing, Commercial, Partners',
    'description': """
Account Invoice Partner Commercial
==================================
Allows partners to be chosen as commercial in accounts, and inherit them by default when 
creating an associated invoice.. 
It also choose the salesperson when creating invoices from stock.picking
Inspired from account_invoice_commercial (Adhoc SA).
    """,
    'author':  'Blanco Martin & Asociados',
    'website': 'http://blancomartin.cl',
    'images': [
    ],
    'depends': [
        'account',
        'l10n_cl_invoice'
    ],
    'data': [
        'views/partner_commercial.xml',
        'data/ir.values.xml'
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: