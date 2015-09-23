# -*- coding: utf-8 -*-
##############################################################################
# Chilean Payroll
# Odoo / OpenERP, Open Source Management Solution
# By Blanco Martín & Asociados - Nelson Ramírez Sánchez (http://blancomartin.cl).
#
# Derivative from Odoo / OpenERP / Tiny SPRL
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

from openerp.osv import osv

class hr_payslip_employees(osv.osv_memory):

    _inherit ='hr.payslip.employees'
    
    def compute_sheet(self, cr, uid, ids, context=None):
        run_pool = self.pool.get('hr.payslip.run')
        if context is None:
            context = {}
        if context.get('active_id'):
            run_data = run_pool.read(cr, uid, context['active_id'], ['indicadores_id'])
        indicadores_id= run_data.get('indicadores_id')
        indicadores_id= indicadores_id and indicadores_id[0] or False
        if indicadores_id:
            context = dict(context, indicadores_id=indicadores_id)
        return super(hr_payslip_employees, self).compute_sheet(cr, uid, ids, context=context)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
