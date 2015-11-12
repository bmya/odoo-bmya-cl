# -*- coding: utf-8 -*-
from openerp import models, fields, api
import re


class res_partner(models.Model):
    _inherit = 'res.partner'

    formated_vat = fields.Char(
        translate=True, string='Printable VAT', compute='_get_f_vat',
        store=True, help='Show formatted vat')

    @api.depends('vat')
    def _get_f_vat(self):
        """
        Retorna el RUT formateado en forma acostumbrada (xx.xxx.xxx-x).
        """
        for record in self:
            record.formated_vat = record.document_number
