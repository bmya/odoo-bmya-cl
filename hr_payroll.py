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

import time
from datetime import date, datetime, timedelta

from openerp.osv import fields, osv
from openerp.tools import float_compare, float_is_zero
from openerp.tools.translate import _

class hr_indicadores_previsionales(osv.osv):
    _name = 'hr.indicadores'
    _description = 'Indicadores Previsionales'
    _columns = {
        'name': fields.char('Nombre', required=True),
        'asignacion_familiar_primer': fields.float('Asignacion Familiar Tramo 1', digits=(16,2), help="Asig Familiar Primer Tramo"),
        'asignacion_familiar_segundo': fields.float('Asignacion Familiar Tramo 2', digits=(16,2), help="Asig Familiar Segundo Tramo"),
        'asignacion_familiar_tercer': fields.float('Asignacion Familiar Tramo 3', digits=(16,2),  help="Asig Familiar Tercer Tramo"),
        'asignacion_familiar_monto_a': fields.float('Monto Tramo Uno', digits=(16,2),  help="Monto A"),
        'asignacion_familiar_monto_b': fields.float('Monto Tramo Dos', digits=(16,2), help="Monto B"),
        'asignacion_familiar_monto_c': fields.float('Monto Tramo Tres', digits=(16,2),  help="Monto C"),
        'contrato_plazo_fijo_empleador': fields.float('Contrato Plazo Fijo Empleador', digits=(16,2),  help="Contrato Plazo Fijo Empleador"),
        'contrato_plazo_indefinido_empleador': fields.float('Contrato Plazo Indefinido Empleador', digits=(16,2),  help="Contrato Plazo Fijo"), 
        'contrato_plazo_indefinido_empleador_otro': fields.float('Contrato Plazo Indefinido 11 anos o mas', digits=(16,2),  help="Contrato Plazo Indefinido 11 anos"),
        'caja_compensacion': fields.float('Caja Compensacion Los Andes', digits=(16,2),  help="Caja de Compensacion"),
        'deposito_convenido': fields.float('Deposito Convenido', digits=(16,2), help="Deposito Convenido"),
        'fonasa': fields.float('Fonasa', digits=(16,2),  help="Fonasa"),
        'mutual_seguridad': fields.float('Mutual Seguridad', digits=(16,2), help="Mutual de Seguridad"),
        'pensiones_ips': fields.float('Pensiones IPS', digits=(16,2),  help="Pensiones IPS"),
        'sueldo_minimo': fields.float('Sueldo Minimo', digits=(16,2),  help="Sueldo Minimo"),
        'sueldo_minimo_otro': fields.float('Sueldo Minimo Menores de 18 y Mayores de 65', digits=(16,2),  help="Sueldo Minimo para Menores de 18 y Mayores a 65"),
 	'tasa_mutual': fields.float('Tasa Mutual', digits=(16,2), help="Tasa AFP Mutual"),
        'tasa_afp_cuprum': fields.float('Cuprum', digits=(16,2),  help="Tasa AFP Cuprum"),
        'tasa_afp_capital': fields.float('Capital', digits=(16,2),  help="Tasa AFP Capital"),
        'tasa_afp_provida': fields.float('ProVida', digits=(16,2),  help="Tasa AFP Provida"),
        'tasa_afp_modelo': fields.float('Modelo', digits=(16,2),  help="Tasa AFP Modelo"),
        'tasa_afp_planvital': fields.float('PlanVital', digits=(16,2),  help="Tasa AFP PlanVital"),
        'tasa_afp_habitat': fields.float('Habitat', digits=(16,2),  help="Tasa AFP Habitat"),
        'tasa_sis_cuprum': fields.float('SIS', digits=(16,2), help="Tasa SIS Cuprum"),
        'tasa_sis_capital': fields.float('SIS', digits=(16,2), help="Tasa SIS Capital"),
        'tasa_sis_provida': fields.float('SIS', digits=(16,2), help="Tasa SIS Provida"),
        'tasa_sis_planvital': fields.float('SIS', digits=(16,2), help="Tasa SIS PlanVital"),
        'tasa_sis_habitat': fields.float('SIS', digits=(16,2), help="Tasa SIS Habitat"),
        'tasa_sis_modelo': fields.float('SIS', digits=(16,2), help="Tasa SIS Modelo"),
        'tasa_independiente_cuprum': fields.float('SIS', digits=(16,2), help="Tasa Independientes Cuprum"),
        'tasa_independiente_capital': fields.float('SIS', digits=(16,2), help="Tasa Independientes Capital"),
        'tasa_independiente_provida': fields.float('SIS', digits=(16,2), help="Tasa Independientes Provida"),
        'tasa_independiente_planvital': fields.float('SIS', digits=(16,2), help="Tasa Independientes PlanVital"),
        'tasa_independiente_habitat': fields.float('SIS', digits=(16,2), help="Tasa Independientes Habitat"),
        'tasa_independiente_modelo': fields.float('SIS', digits=(16,2), help="Tasa Independientes Modelo"),
        'tope_anual_apv': fields.float('Tope Anual APV', digits=(16,2),  help="Tope Anual APV"),
        'tope_mensual_apv': fields.float('Tope Mensual APV', digits=(16,2),  help="Tope Mensual APV"),
        'tope_imponible_afp': fields.float('Tope imponible AFP', digits=(16,2),  help="Tope Imponible AFP"),
        'tope_imponible_ips': fields.float('Tope Imponible IPS', digits=(16,2),  help="Tope Imponible IPS"),
        'tope_imponible_salud': fields.float('Tope Imponible Salud', digits=(16,2),  help="Tope Imponible Salud"),
        'tope_imponible_seguro_cesantia': fields.float('Tope Imponible Seguro Cesantia', digits=(16,2),  help="Tope Imponible Seguro de Cesantia"),
        'uf': fields.float('UF', digits=(16,2), required=True, help="UF fin de Mes"),
        'utm': fields.float('UTM', digits=(16,2), required=True, help="UTM Fin de Mes"),
        'uta': fields.float('UTA', digits=(16,2),  help="UTA Fin de Mes"),
        'uf_otros': fields.float('UF Otros', digits=(16,2), help="UF Seguro Complementario"),
    
}

class hr_payslip(osv.osv):
    '''
    Pay Slip
    '''
    _inherit = 'hr.payslip'
    _description = 'Pay Slip'

    _columns = {
        'indicadores_id': fields.many2one('hr.indicadores', 'Indicadores',states={'draft': [('readonly', False)]}, readonly=True, required=True),
        
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        else:
            vals.update({'indicadores_id': context.get('indicadores_id')})
        return super(hr_payslip, self).create(cr, uid, vals, context=context)

class hr_payslip_run(osv.osv):

    _inherit = 'hr.payslip.run'
    _description = 'Payslip Run'
    _columns = {
        
    'indicadores_id': fields.many2one('hr.indicadores', 'Indicadores',states={'draft': [('readonly', False)]}, readonly=True, required=True),

    }

class hr_isapre(osv.osv):
    _name = 'hr.isapre'
    _description = 'Isapres'
    _columns = {
        'name': fields.char('Nombre', required=True),
        'rut': fields.char('RUT', required=True),
    }

class hr_afp(osv.osv):
    _name = 'hr.afp'
    _description = 'Fondos de Pension'
    _columns = {
        'name': fields.char('Nombre', required=True),
        'rut': fields.char('RUT', required=True),
        'rate': fields.float('Tasa', required=True),
        'sis': fields.float('Aporte Empresa', required=True),
        'independiente': fields.float('Independientes', required=True),
    }



class hr_contract(osv.osv):

    _inherit = 'hr.contract'
    _description = 'Employee Contract'
    _columns = {
        'afp_id':fields.many2one('hr.afp', 'AFP'),
        'aporte_voluntario': fields.float('Aporte Voluntario', help="Aporte Voluntario al ahorro individual"),
        'anticipo_sueldo': fields.float('Anticipo de Sueldo',  help="Anticipo De Sueldo Realizado Contablemente"),
        'carga_familiar': fields.integer('Carga Familiar', help="Carga Familiar para el calculo de asignacion familiar"),
        'colacion': fields.float('Colacion',  help="Colacion"),
        'isapre_id':fields.many2one('hr.isapre', 'ISAPRE'),
        'isapre_cotizacion_uf': fields.float('Cotizacion UF', digits=(16,2), help="Cotizacion Pactada en UF"),
        'movilizacion': fields.float('Movilizacion',  help="Movilizacion"),
        'mutual_seguridad': fields.boolean('Mutual Seguridad'),
        'otro_no_imp': fields.float('Otros No Imponible',  help="Otros Haberes No Imponibles"),
        'otros_imp': fields.float('Otros Imponible', help="Otros Haberes Imponibles"),
        'pension': fields.boolean('Pensionado'),
        'seguro_complementario_id':fields.many2one('hr.seguro.complementario', 'Seguro Complementario'),
        'seguro_complementario_cotizacion_uf': fields.float('Cotizacion UF', digits=(16,2), help="Cotizacion Pactada en UF"),
        'viatico_santiago': fields.float('Viatico Santiago', digits=(16,2),  help="Viatico Santiago"),

    }



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: