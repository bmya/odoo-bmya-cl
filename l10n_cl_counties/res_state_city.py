# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012 Cubic ERP - Teradata SAC. (http://cubicerp.com).
#    Copyright (C) 2016 Blanco Martín & Asociados - Odoo Chile Community
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from openerp.osv import fields, osv


class res_state_city(osv.osv):

    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        res = []
        for city in self.browse(cr, uid, ids, context=context):
            res.append((city.id, (city.code and '[' + city.code + '] ' or '') + city.name))
        
        return res
        
    
    def complete_name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        args = args[:]
        ids = []
        if name:
            ids = self.search(cr, user, [('name', operator, name)]+ args, limit=limit)
            if not ids and len(name.split()) >= 2:
                #Separating code and name of account for searching
                operand1,operand2 = name.split(': ',1) #name can contain spaces e.g. OpenERP S.A.
                ids = self.search(cr, user, [('name', operator, operand2)]+ args, limit=limit)
        else:
            ids = self.search(cr, user, args, context=context, limit=limit)
        return self.name_get(cr, user, ids, context=context)
    
    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        if not ids:
            return []
        res = []
        for city in self.browse(cr, uid, ids, context=context):
            data = []
            acc = city
            while acc:
                data.insert(0, acc.name)
                if hasattr(acc,'state_id'):
                    acc = acc.state_id
                else :
                    acc = acc.parent_id
            data = ' / '.join(data)
            res.append((city.id, data))
        return dict(res)
        
    _name = 'res.country.state.city'
    _description = "City of state"
    _columns = {
            'name': fields.char('City Name',help='The City Name.',required=True),
            'code': fields.char('City Code', size=32,help='The city code.\n', required=True),
            'complete_name': fields.function(_name_get_fnc, method=True, type="char", string='Complete Name', fnct_search=complete_name_search),
            'country_id': fields.many2one('res.country', 'Country', required=True),
            'state_id': fields.many2one('res.country.state','State', select=True, domain="[('country_id','=',country_id),('type','=','normal')]"),
            'type': fields.selection([('view','View'), ('normal','Normal')], 'Type'),
        }
    _defaults = {
            'type': 'normal',
        }