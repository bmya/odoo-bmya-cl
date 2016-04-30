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

from openerp import models, fields, api


class invoice_turn(models.Model):
    _inherit = "account.invoice"


    @api.one
    @api.depends('partner_id')
    def _get_available_turns(self):
        self.ensure_one()
        available_turn_ids = self.partner_id.partner_activities_ids
        for turn in available_turn_ids:
            self.invoice_turn = turn.id


    invoice_turn = fields.Many2one(
        'partner.activities',
        'Giro Receptor',
        readonly=True,
        store=True,
        states={'draft': [('readonly', False)]},
        compute=_get_available_turns)




