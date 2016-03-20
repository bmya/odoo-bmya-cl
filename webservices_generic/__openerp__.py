# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Web Services Generic Tool - By Blanco Martín & Asociados
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#	 This module authored by Daniel Blanco, Blanco Martín & Asociados
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
    'name': 'Web Services Generic Tool',
    'version': '0.0',
    'category': 'Tools',
    'complexity': "easy",
    'description': "Data Model that allows to act as a repository for generic web services connection",
    'author': 'Blanco Martin & Asociados',
    'website': 'http://blancomartin.cl',
    "external_dependencies": {
        'python': ['urllib3', 'pysftp']
    },
    'data': [
        'views/ws_servers.xml',
        # 'data/web.services.xml',
        'data/webservices.server.csv',
        'security/ir.model.access.csv',
    ],
    'license': 'AGPL-3',
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
