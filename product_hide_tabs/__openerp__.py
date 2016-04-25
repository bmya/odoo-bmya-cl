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
    'name': 'Product Hide Tabs',
    'version': '8.0.0.1.0',
    'category': 'Products',
    'sequence': 14,
    'summary': 'Invoicing, Commercial, Partners',
    'description': """
Product Hide Tabs
=================
This is a security feature, in order to hide sale/inventory tabs in product
form view.
    """,
    'author':  'Blanco Martin & Asociados',
    'website': 'http://blancomartin.cl',
    'images': [
    ],
    'depends': [
        'stock',
    ],
    'data': [
        'views/product_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}