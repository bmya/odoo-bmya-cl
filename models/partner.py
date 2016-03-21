# -*- coding: utf-8 -*-
from openerp import fields, models, api
import re


class res_partner(models.Model):
    _inherit = 'res.partner'

    def _get_default_tp_type(self):
        return self.env.ref('l10n_cl_invoice.res_IVARI').id

    def _get_default_doc_type(self):
        return self.env.ref('l10n_cl_invoice.dt_RUT').id

    responsability_id = fields.Many2one(
        'sii.responsability', 'Responsability', default=_get_default_tp_type)
    document_type_id = fields.Many2one(
        'sii.document_type', 'Document type', default=_get_default_doc_type)
    document_number = fields.Char('Document number', size=64)
    
    start_date = fields.Date('Start-up Date')

    tp_sii_code = fields.Char('Tax Payer SII Code', compute='_get_tp_sii_code',
        readonly=True)

    is_company = fields.Boolean('Is Company', default=True)

    @api.multi
    @api.onchange('responsability_id')
    def _get_tp_sii_code(self):
        for record in self:
            record.tp_sii_code=str(record.responsability_id.tp_sii_code)


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
