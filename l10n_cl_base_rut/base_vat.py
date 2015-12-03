# -*- coding: utf-8 -*-
from openerp import models, fields, api
import re


class res_partner(models.Model):
    _inherit = 'res.partner'

    formated_vat = fields.Char(
        translate=True, string='Printable VAT',
        store=True, help='Show formatted vat')

    @api.onchange('formated_vat')
    def onchange_document(self):
        mod_obj = self.env['ir.model.data']
        formated_vat = (
            re.sub('[^1234567890Kk]', '',
            str(self.formated_vat))).zfill(9).upper()

        self.vat = 'CL%s' % formated_vat
        
        self.formated_vat = formated_vat[0:2] + '.' + formated_vat[2:5] + '.' + formated_vat[5:8] +'-' + formated_vat[-1]
