# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
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
    'name': u'Clean Cancelled Invoice Number (Chilean Compatibility Version)',
    'version': '8.0.1.1.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': u'Invoicing, Number, Cancelled',
    'description': u"""
Clean Cancelled Invoice Number
Adds a button on invoice to allow clean number to cancelled invoices in order to:
* Regenerate the invoice number with new sequence number
* Delete the invoice
- This is a fork of account_clean_cancelled_invoice_number from Ingeniería Adhoc,
but adapted by Blanco Martín & Asociados for Chilean localization compatibility.
    """,
    'author':  u'ADHOC SA, - Blanco Martín & Asociados',
    'website': 'www.adhoc.com.ar',
    'depends': [
        'account_cancel'
    ],
    'data': [
        'views/account_invoice_view.xml',
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