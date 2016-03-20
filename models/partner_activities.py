# -*- coding: utf-8 -*-
##############################################################################
# Chilean SII Partner Activities
# Odoo / OpenERP, Open Source Management Solution
# By Blanco Martín & Asociados - (http://blancomartin.cl).
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

from openerp import models, fields


class partner_activities(models.Model):

    _description = 'SII Economical Activities'
    _name = 'partner.activities'

    code = fields.Char('Activity Code', required=True, translate=True)

    parent_id = fields.Many2one(
        'partner.activities', 'Parent Activity', select=True,
        ondelete='cascade')

    name = fields.Char('Nombre Completo', required=True, translate=True)

    vat_affected = fields.Selection(
        (('SI', 'Si'), ('NO', 'No'), ('ND', 'ND')), 'VAT Affected',
        required=True, translate=True, default='SI')

    tax_category = fields.Selection(
        (('1', '1'), ('2', '2'), ('ND', 'ND')), 'TAX Category', required=True,
        translate=True, default='1')

    internet_available = fields.Boolean('Available at Internet')

    active = fields.Boolean(
        'Active', help="Allows you to hide the activity without removing it.")

    partner_ids = fields.Many2many(
        'res.partner', id1='activities_id', id2='partner_id',
        string='Partners')

    _defaults = {
        'active': 1,
        'internet_available': 1
    }


class partner_turns(models.Model):

    _description = 'Partner registered turns'
    _inherit = 'res.partner'

    partner_activities_ids = fields.Many2many(
        'partner.activities', id1='partner_id', id2='activities_id',
        string='Activities Names')

class company_turns(models.Model):

    _description = 'Company registered turns'
    _inherit = 'res.company'

    company_activities_ids = fields.Many2many(
        string='Activities Names',
        related='partner_id.partner_activities_ids',
        relation='partner.activities')