# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Tool	
#
#    Copyright (c) 2015 Blanco Martin y Asociados - Nelson Ramírez Sánchez http://blancomartin.cl
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Chile Localization Chart Account BMyA',
    'author': u'Blanco Martin & Asociados - Nelson Ramírez Sánchez - Daniel Blanco',
    'website': 'http://blancomartin.cl',
    # 'depends': ['account_chart'],
    'license': 'AGPL-3',
    'version': '1.0',
    'category': 'Localization/Chile',
    'description': """
Chilean accounting chart and tax localization.
==============================================
Plan contable chileno e impuestos de acuerdo a disposiciones vigentes,
basado en plan de cuentas de Superintendencia de Valores y Seguros de
Chile, con algunas cuentas agregadas en base a experiencias de
implementación
    """,   
    'category': 'Localization/Account Charts',
    'data': [
        'data/l10n_cl_bmya_wizard.xml',
        'data/account_tax_code.xml',
        'data/l10n_cl_chart_svs.xml',
        'data/account_tax.xml',
    ],
    'demo': [],
    'active': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
