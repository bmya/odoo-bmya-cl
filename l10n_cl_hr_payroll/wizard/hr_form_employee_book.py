# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution Chilean Payroll
#
#    Copyright (c) 2015 Blanco Martin y Asociados - Nelson Ramírez Sánchez
#    Daniel Blanco
#    http://blancomartin.cl
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
from openerp import models, fields
import time


class hr_salary_employee_bymonth(models.TransientModel):

    _name = 'hr.salary.employee.month'
    _description = 'Libro de Remuneraciones Haberes'

    end_date = fields.Date('End Date', required=True)

    _defaults = {

        'end_date': lambda *a: time.strftime('%Y-%m-%d'),

    }

    def print_report(self, cr, uid, ids, context=None):
        """
         To get the date and print the report
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return: return report
        """
        if context is None:
            context = {}
        datas = {'ids': context.get('active_ids', [])}

        res = self.read(cr, uid, ids, context=context)
        res = res and res[0] or {}
        datas.update({'form': res})
        return self.pool['report'].get_action(
            cr, uid, ids, 'l10n_cl_hr_payroll.report_hrsalarybymonth',
            data=datas, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
