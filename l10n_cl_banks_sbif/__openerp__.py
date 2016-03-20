# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2004-2015 Odoo (<http://odoo.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    Copyright (c) 2015 Blanco Martin y Asociados http://blancomartin.cl
#    This module authored by Daniel Blanco, Blanco Martín & Asociados
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
    'category': 'Localization/Banks',
    'description': '''
    Update Chilean Banks and add their Official codes, according to SBIFs codes
    ''',
    'author': u'Blanco Martin & Asociados',
    'website': 'http://blancomartin.cl',
    'depends': ['account', 'account_chart'],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Chile - Bancos con codificación oficial de SBIF',
    'test': [],
    'data': [
        'data/res.bank.csv', 'view/res_bank_sbif.xml'
    ],
    'version': '0.1.001',
}
