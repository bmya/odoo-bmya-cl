# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Cubic ERP - Teradata SAC.
#    Copyright (C) 2016 Blanco Martín & Asociados - Odoo Chile Community
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
    "name": "Chile Localization Regions, Cities and Counties",
    "version": "1.1",
    "description": """
Chilean Regions, Cities and Counties .

Lista de regiones, ciudades y comunas de Chile.
    """,
    "author": "Cubic ERP, Blanco Martín & Asociados, Odoo Chile Community",
    "website": "http://odoochile.org",
    "category": "Localization/Toponyms",
    "depends": [
            "base_state_ubication",
        ],
    "data": [
        "l10n_cl_counties_data.xml",
        ],
    'init_xml': [
        'query.sql'
        ],
    "active": False,
    "installable": True,
}
