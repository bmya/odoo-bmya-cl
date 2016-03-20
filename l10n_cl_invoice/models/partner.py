# -*- coding: utf-8 -*-
from openerp import fields, models, api
import re


class res_partner(models.Model):
    _inherit = 'res.partner'

    responsability_id = fields.Many2one(
        'sii.responsability', 'Resposability')
    document_type_id = fields.Many2one(
        'sii.document_type', 'Document type')
    document_number = fields.Char('Document number', size=64)
    
    start_date = fields.Date('Start-up Date')

    @api.onchange('document_number', 'document_type_id')
    def onchange_document(self):
        mod_obj = self.env['ir.model.data']
        if self.document_number and ((
            'sii.document_type',
            self.document_type_id.id) == mod_obj.get_object_reference(
                'l10n_cl_invoice', 'dt_RUT') or ('sii.document_type',
                self.document_type_id.id) == mod_obj.get_object_reference(
                    'l10n_cl_invoice', 'dt_RUN')):
            document_number = (
                re.sub('[^1234567890Kk]', '', str(
                    self.document_number))).zfill(9).upper()
            self.vat = 'CL%s' % document_number
            self.document_number = '%s.%s.%s-%s' % (
                document_number[0:2], document_number[2:5],
                document_number[5:8], document_number[-1])
            
        elif self.document_number and (
            'sii.document_type',
            self.document_type_id.id) == mod_obj.get_object_reference(
                'l10n_cl_invoice', 'dt_Sigd'):
            self.document_number = ''
