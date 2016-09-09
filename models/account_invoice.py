# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def clean_internal_number(self):
        self.ensure_one()
        self.write({
        	'internal_number':False,
            'sii_document_number':False,
            'sii_document_class_id': False,
            'sii_batch_number': False,
            'sii_barcode': False,
            'sii_barcode_img': False,
            'sii_message': False,
            'sii_xml_request': False,
            'sii_xml_response1': False,
            'sii_xml_response2': False,
            'sii_send_ident': False,
            'sii_result': False})