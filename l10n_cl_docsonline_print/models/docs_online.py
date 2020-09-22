import base64
import json
import logging

import requests
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class DocsOnlinePrint(models.Model):
    _inherit = 'account.move'

    docs_online_token = fields.Char('URL DTE', copy=False)

    def _get_pdf_docs_online(self, file_upload, transferable=0):
        host = 'http://www2.documentosonline.cl'
        headers = {
            'Accept': u'*/*',
            'Accept-Encoding': u'gzip, deflate, compress',
            'Connection': u'close',
            'Content-Type': u'multipart/form-data;boundary=33b4531a79be4b278de5f5688fab7701',
            'User-Agent': u'python-requests/2.2.1 CPython/2.7.6 Darwin/13.2.0', }
        r = requests.post(host + '/dte/hgen/token', files=dict(file_upload=file_upload))
        _logger.info('request: %s' % r)
        _logger.info('request test: %s' % r.text)
        if r.status_code == 200:
            _logger.info(json.loads(r.text)['token'])
            self.docs_online_token = host + '/dte/hgen/html/%s' % json.loads(r.text)['token']
            headers['Connection'] = 'keep-alive'
            headers['Content-Type'] = 'application/json'
            data = {'params': json.loads(r.text)}
            if transferable == 1:
                data['params']['cedible'] = 1
            _logger.info('data: %s' % data)
            r = requests.post(host + '/dte/jget', headers=headers, data=json.dumps(data))
            if r.status_code == 200:
                _logger.info(r.json())
                document_pdf = json.loads(r.json()['result'])['pdf']
                begin = 'DTE_' if not transferable else 'DTE_CED_'
                attachment_name = begin + 'F%sT%s.pdf' % (
                    self.l10n_latam_document_number, self.l10n_latam_document_type_id.code)
                attachment_obj = self.env['ir.attachment'].sudo()
                record_id = self.id
                attachment_pdf_id = attachment_obj.create({
                    'name': attachment_name + '.pdf',
                    'datas': document_pdf,
                    'datas_fname': attachment_name + '.pdf',
                    'res_model': self._name,
                    'res_id': record_id,
                    'type': 'binary', })
                return attachment_pdf_id
        return False

    def action_invoice_sent(self):
        self.ensure_one()
        if self.company_id.country_id != self.env.ref('base.cl'):
            return super().action_invoice_sent()
        attachment_obj = self.env['ir.attachment'].sudo()
        invoice_file = 'F%sT%s' % (int(self.l10n_latam_document_number), self.l10n_latam_document_type_id.code)
        invoice_pdf_file = 'DTE_%s.pdf' % invoice_file
        # invoice_pdf_transferable_file = 'DTE_CED_%s.pdf' % invoice_file
        search_domain = [['res_model', '=', self._name], ['res_id', '=', self.id]]
        attachment_pdf_id = attachment_obj.search(
            search_domain + [['name', '=', invoice_pdf_file]], order='id desc', limit=1)
        if not attachment_pdf_id:
            invoice_xml_file = '%s.xml' % invoice_file
            invoice_sii_file = 'SII_%s.xml' % invoice_file
            search_domain += [['name', 'in', [invoice_xml_file, invoice_sii_file]]]
            _logger.info('SEARCH DOMAIN: %s' % search_domain)
            attachment_xml_id = attachment_obj.search(
                search_domain, order='id desc', limit=1)
            if attachment_xml_id:
                attachment = self._get_pdf_docs_online(base64.b64decode(attachment_xml_id.datas))
            else:
                raise UserError('The invoice has not been generated yet')
        else:
            attachment = attachment_id[0]
        _logger.info('Downloading attachment in PDF...')
        if attachment:
            url = '/web/content/%s?download=true' % attachment.id
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'new', }
        else:
            raise UserError('No se puede descargar el PDF')

        # return {
        #     'name': _('Send Invoice'),
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'account.invoice.send',
        #     'views': [(compose_form.id, 'form')],
        #     'view_id': compose_form.id,
        #     'target': 'new',
        #     'context': ctx,
        # }


    # def transferable_print_docs_online(self):
    #     for self in self:
    #         attachment_obj = record.env['ir.attachment'].sudo()
    #         attachment_id = attachment_obj.search(
    #             [('name', 'ilike', 'DTE_CED_'),
    #              ('name', 'ilike', 'pdf'),
    #              ('res_model', '=', record._name),
    #              ('res_id', '=', record.id)], order='id desc', limit=1)
    #         if not attachment_id:
    #             if True:  # try:
    #                 _logger.info('document_print_docs_online: xml_envio: %s' % record.sii_xml_request.xml_envio)
    #                 if not record.sii_xml_request.xml_envio and \
    #                         record.document_code not in {'39', '41'}:
    #                     # este es el codigo que crea el archivo de intercambio (contribuyente)
    #                     xml_envio = record.create_exchange()
    #                 elif record.document_code in {'39', '41'}:
    #                     xml_envio = record.sii_xml_dte
    #                 else:
    #                     xml_envio = record.sii_xml_request.xml_envio
    #                 attachment = record.get_pdf_docs_online(xml_envio, 1)
    #             else:  # except AttributeError:
    #                 _logger.info('attribute error')
    #                 attachment = self.get_pdf_docs_online(self.sii_xml_dte, 1)
    #                 # attachment = self.get_pdf_docs_online(self.sii_xml_request.xml_envio, 1)
    #         else:
    #             attachment = attachment_id[0]
    #         _logger.info('Downloading attachment in PDF...')
    #         url = '/web/content/%s?download=true' % attachment.id
    #         _logger.info(url)
    #         return {
    #             'type': 'ir.actions.act_url',
    #             'url': url,
    #             'target': 'new', }

    # @api.multi
    # def action_invoice_sent_docs_online(self):
    #     """
    #     Open a window to compose an email, with the edi invoice template
    #     message loaded by default
    #     """
    #     if self.env.user.company_id.localization != 'chile':
    #         # return super(DocsOnlinePrint, self).action_invoice_sent()
    #         self.action_invoice_sent()
    #     self.ensure_one()
    #     if not self.sii_xml_request.xml_envio and \
    #                 self.journal_document_type_id.document_type_id.code not in {'39', '41'}:
    #         # este es el codigo que crea el archivo de intercambio (contribuyente)
    #         xml_envio = self.create_exchange()
    #     elif self.document_code in {'39', '41'}:
    #         xml_envio = self.sii_xml_dte
    #     else:
    #         xml_envio = self.sii_xml_request.xml_envio
    #     self.get_pdf_docs_online(xml_envio)
    #     template = self.env.ref('l10n_cl_docsonline_print.email_template_edi_invoice', False)
    #     compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
    #     att = self._create_attachment()
    #     atts = []
    #     if template.attachment_ids:
    #         for a in template.attachment_ids:
    #             atts.append(a.id)
    #     atts.append((6, 0, [att.id]))
    #     attachment_id = self.env['ir.attachment'].search([
    #         ('res_model', '=', self._name),
    #         ('res_id', '=', self.id),
    #         ('name', 'not like', 'DTE_CED%'),
    #         ('name', 'like', 'DTE_%.pdf'), ],
    #         order='id desc',
    #         limit=1, )
    #     atts.append(attachment_id.id)
    #     ctx = dict(
    #         default_model='account.invoice',
    #         default_res_id=self.id,
    #         default_use_template=bool(template),
    #         default_template_id=template.id,
    #         default_composition_mode='comment',
    #         default_attachment_ids=atts,
    #         mark_invoice_as_sent=True, )
    #     return {
    #         'name': _('Compose Email'),
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'mail.compose.message',
    #         'views': [(compose_form.id, 'form')],
    #         'view_id': compose_form.id,
    #         'target': 'new',
    #         'context': ctx, }






# class SendQueue(models.Model):
#     _inherit = 'sii.send_queue'
#
#     def send_template_email(self, doc):
#         # este es el codigo que crea el archivo de intercambio (contribuyente)
#         atts = [doc._create_attachment().id]
#         atts.append(doc.get_pdf_docs_online(doc.sii_xml_request.xml_envio).id)
#         template = self.env.ref('l10n_cl_docsonline_print.email_template_edi_invoice', False).sudo()
#         if template.attachment_ids:
#             for a in template.attachment_ids:
#                 atts.append(a.id)
#         mail_id = template.send_mail(
#             doc.id,
#             force_send=True,
#             email_values={'attachment_ids': atts})
#         _logger.info('mass email from send queue.... mail_id: %s' % mail_id)
#         doc.sii_result = 'Aceptado'
#         return True
