# -*- coding: utf-8 -*-
from openerp import models, fields, api
import re


class res_partner(models.Model):
    _inherit = 'res.partner'

    formated_vat = fields.Char(
        translate=True, string='Printable VAT', store=True,
        help='Show formatted vat')

    def check_vat_cl (self, vat):
        body, vdig = '', ''
        if len(vat) > 9:
            vat = vat.replace('-','',1).replace('.','',2)
        if len(vat) != 9:
            return False
        else:
            body, vdig = vat[:-1], vat[-1].upper()
        try:
            vali = range(2,8) + [2,3]
            operar = '0123456789K0'[11 - (
                sum([int(digit)*factor for digit, factor in zip(
                    body[::-1],vali)]) % 11)]
            if operar == vdig:
                return True
            else:
                return False
        except IndexError:
            return False

    @api.onchange('formated_vat')
    def onchange_document(self):
        mod_obj = self.env['ir.model.data']
        formated_vat = (
            re.sub('[^1234567890Kk]', '',
            str(self.formated_vat))).zfill(9).upper()

        self.vat = 'CL%s' % formated_vat
        
        self.formated_vat = '%s.%s.%s-%s' % (
            formated_vat[0:2], formated_vat[2:5], formated_vat[5:8],
            formated_vat[-1])
