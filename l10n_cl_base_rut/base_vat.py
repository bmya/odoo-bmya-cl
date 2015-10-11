# -*- coding: utf-8 -*-
from openerp import models, fields, api
import locale

# locale.setlocale(locale.LC_ALL,'es_CL.utf-8')


class res_partner(models.Model):
    _inherit = 'res.partner'

    formated_vat = fields.Char(
        translate=True, string='Printable VAT', compute='_get_formated_vat',
        store=True, help='Show formatted vat')

    @api.multi
    def _get_formated_vat(self):
        """
        Retorna el RUT formateado en forma acostumbrada (xx.xxx.xxx-x).
        """
        res = {}
        for partner in self:
            res[partner.id] = self.format_vat_cl(partner.vat)
        return res

    def format_vat(self,vat):
        try:
            return locale.format('%d',int(float(vat[2:10])),1)+'-' + vat[10:]
        except:
            return "            "
