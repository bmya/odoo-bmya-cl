# -*- coding: utf-8 -*-
from openerp import osv, models, fields, api, _
from openerp.osv import fields as old_fields
from openerp.exceptions import except_orm, Warning
from openerp.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class account_invoice(models.Model):
    _inherit = "account.invoice"


    '''
    Función que define el diario por defecto.
    Se usa como función default y es llamada por los onchange que correspondan
    @autor: Localizacion Argentina y adaptada por Daniel Blanco
    (daniel[at]blancomartin.cl) para localizacion Chilena y api v8
    @version: 2016-07-25
    '''
    def _get_operation_type(self, invoice_type):
        if invoice_type in ['in_invoice', 'in_refund']:
            operation_type = 'purchase'
        elif invoice_type in ['out_invoice', 'out_refund']:
            operation_type = 'sale'
        else:
            operation_type = False
        return operation_type


    '''
    Función que define el giro emisor por defecto.
    Se usa como función default y es llamada por los onchange que correspondan
    @autor: Daniel Blanco daniel[at]blancomartin.cl
    @version: 2016-07-25
    '''
    @api.model
    def _set_default_turn_issuer(self):
        available_turns = self._get_available_issuer_turns()
        for turn in available_turns:
            # devuelve el primero de los giros
            return turn

    # funcion de muestra. Esta está en account:
    # @api.model
    # def _default_journal(self):
    #     inv_type = self._context.get('type', 'out_invoice')
    #     inv_types = inv_type if isinstance(inv_type, list) else [inv_type]
    #     company_id = self._context.get('company_id',
    #                                    self.env.user.company_id.id)
    #     domain = [
    #         ('type', 'in', filter(None, map(TYPE2JOURNAL.get, inv_types))),
    #         ('company_id', '=', company_id),
    #     ]
    #     return self.env['account.journal'].search(domain, limit=1)

    @api.model
    def _get_available_issuer_turns(self, company_id=False, journal_id=False):
        # opcion mala: trae todos los giros de la compañia, pero no
        # las que estan vinculadas al diario
        issuer_turns = self.env.user.company_id.company_activities_ids
        self._get_available_journal_document_class(self.partner_id)
        return issuer_turns


    '''
    Función que define el documento a emitir por defecto.
    Se usa como función default y es llamada por los onchange que correspondan
    @autor: Daniel Blanco daniel[at]blancomartin.cl
    @version: 2016-07-25
    '''
    def _set_default_tax_doc(self):
        _logger.info('Entrando a funcion _set_default_tax_doc')
        pass

    @api.model
    def _get_valid_document_letters(
            self, partner_id=False, operation_type='sale',company_id=False,
            vat_affected='SI', invoice_type='out_invoice'):

        print('get_valid_document_letters')

        document_letter_obj = self.env['sii.document_letter']
        user = self.env['res.users'].browse()
        partner = self.env['res.partner'].browse()

        if not partner_id or not company_id or not operation_type:
            return []

        partner = partner.commercial_partner_id

        company = self.env['res.company'].browse()

        if operation_type == 'sale':
            issuer_responsability_id = company.partner_id.responsability_id.id
            receptor_responsability_id = partner.responsability_id.id
            if invoice_type == 'out_invoice':
                if vat_affected == 'SI':
                    domain = [
                        ('issuer_ids', '=', issuer_responsability_id),
                        ('receptor_ids', '=', receptor_responsability_id),
                        ('name', '!=', 'C')]
                else:
                    domain = [
                        ('issuer_ids', '=', issuer_responsability_id),
                        ('receptor_ids', '=', receptor_responsability_id),
                        ('name', '=', 'C')]

            else:
                # nota de credito de ventas
                domain = [
                    ('issuer_ids', '=', issuer_responsability_id),
                    ('receptor_ids', '=', receptor_responsability_id)]

        elif operation_type == 'purchase':
            issuer_responsability_id = partner.responsability_id.id
            receptor_responsability_id = company.partner_id.responsability_id.id
            if invoice_type == 'in_invoice':
                print('responsabilidad del partner')
                if issuer_responsability_id == self.env.ref(
                        'l10n_cl_invoice', 'res_BH')[1]:
                    print('el proveedor es de segunda categoria y emite boleta de honorarios')
                else:
                    print('el proveedor es de primera categoria y emite facturas o facturas no afectas')

                domain = [
                    ('issuer_ids', '=', issuer_responsability_id),
                    ('receptor_ids', '=', receptor_responsability_id)]
            else:
                # nota de credito de compras
                domain = ['|',('issuer_ids', '=', issuer_responsability_id),
                              ('receptor_ids', '=', receptor_responsability_id)]
        else:
            raise except_orm(_('Operation Type Error'),
                             _('Operation Type Must be "Sale" or "Purchase"'))

        # TODO: fijar esto en el wizard, o llamar un wizard desde aca
        # if not company.partner_id.responsability_id.id:
        #     raise except_orm(_('You have not settled a tax payer type for your\
        #      company.'),
        #      _('Please, set your company tax payer type (in company or \
        #      partner before to continue.'))

        document_letter_ids = document_letter_obj.search(domain)
        return document_letter_ids

    def get_document_class_default(self, document_classes):
        print('entra en metodo get_document_class_default')
        if self.turn_issuer.vat_affected not in ['SI']:
            # es no afecta
            print('document class default es no afecta')
            exempt_ids = [
                self.env.ref('l10n_cl_invoice.dc_y_f_dtn').id,
                self.env.ref('l10n_cl_invoice.dc_y_f_dte').id]
            for document_class in document_classes:
                if document_class.sii_document_class_id.id in exempt_ids:
                    document_class_id = document_class.id
                    break
                else:
                    document_class_id = document_classes.ids[0]
        else:
            print('document class default es afecta')
            document_class_id = document_classes.ids[0]
        return document_class_id

    @api.multi
    @api.onchange('partner_id', 'journal_id')
    @api.depends('partner_id', 'journal_id')
    def _get_available_journal_document_class(self, partner_id=False):
        for inv in self:
            print('loop: ')
            print(inv.partner_id)
            print(inv.journal_id)
            print('entra a la funcion _get_available_journal_document_class')
            print(inv.turn_issuer)
            issuer_turns = inv.env.user.company_id.company_activities_ids
            print(inv.turn_issuer.vat_affected)
            invoice_type = inv.type
            document_class_ids = []
            document_class_id = False

            inv.available_journal_document_class_ids = inv.env[
                'account.journal.sii_document_class']
            #raise Warning(inv.available_journal_document_class_ids)
            if invoice_type in [
                    'out_invoice', 'in_invoice', 'out_refund', 'in_refund']:
                operation_type = inv._get_operation_type(invoice_type)

            if inv.use_documents:
                letter_ids = inv._get_valid_document_letters(
                    inv.partner_id.id, operation_type, inv.company_id.id,
                    inv.turn_issuer.vat_affected, invoice_type)

                domain = [
                    ('journal_id', '=', inv.journal_id.id),
                    '|', ('sii_document_class_id.document_letter_id',
                          'in', letter_ids),
                         ('sii_document_class_id.document_letter_id',
                          '=', False)]

                # If document_type in context we try to serch specific document
                # document_type = inv._context.get('document_type', False)
                # en este punto document_type siempre es falso.
                # TODO: revisar esta opcion
                #if document_type:
                #    document_classes = inv.env[
                #        'account.journal.sii_document_class'].search(
                #        domain + [('sii_document_class_id.document_type', '=', document_type)])
                #    if document_classes.ids:
                #        # revisar si hay condicion de exento, para poner como primera alternativa estos
                #        document_class_id = inv.get_document_class_default(document_classes)
                # For domain, we search all documents
                # raise Warning(domain)
                document_classes = inv.env[
                    'account.journal.sii_document_class'].search(domain)
                document_class_ids = document_classes.ids

                # If not specific document type found, we choose another one
                if not document_class_id and document_class_ids:
                    # revisar si hay condicion de exento, para poner como primera alternativa estos
                    # to-do: manejar más fino el documento por defecto.
                    print('llamada a document class default')
                    document_class_id = inv.get_document_class_default(
                        document_classes)

                # incorporado nuevo, para la compra
                if operation_type == 'purchase':
                    inv.available_journals = []

            inv.available_journal_document_class_ids = document_class_ids
            inv.journal_document_class_id = document_class_id

    @api.model
    def _printed_prices(self):
        res = {}

        for invoice in self.browse():
            printed_amount_untaxed = invoice.amount_untaxed
            printed_tax_ids = [x.id for x in invoice.tax_line]

            vat_amount = sum([
                x.tax_amount for x in invoice.tax_line if x.tax_code_id.parent_id.name == 'IVA'])

            other_taxes_amount = sum(
                line.other_taxes_amount for line in invoice.invoice_line)
            exempt_amount = sum(
                line.exempt_amount for line in invoice.invoice_line)
            vat_tax_ids = [
                x.id for x in invoice.tax_line if x.tax_code_id.parent_id.name == 'IVA']

            if not invoice.vat_discriminated:
                printed_amount_untaxed = sum(
                    line.printed_price_subtotal for line in invoice.invoice_line)
                printed_tax_ids = [
                    x.id for x in invoice.tax_line if x.tax_code_id.parent_id.name != 'IVA']
            res[invoice.id] = {
                'printed_amount_untaxed': printed_amount_untaxed,
                'printed_tax_ids': printed_tax_ids,
                'printed_amount_tax': invoice.amount_total - printed_amount_untaxed,
                'vat_tax_ids': vat_tax_ids,
                'vat_amount': vat_amount,
                'other_taxes_amount': other_taxes_amount,
                'exempt_amount': exempt_amount,
            }
        return res

    _columns = {
        'printed_amount_tax': old_fields.function(
            _printed_prices, type='float',
            digits_compute=dp.get_precision('Account'),
            string='Tax', multi='printed',),
        'printed_amount_untaxed': old_fields.function(
            _printed_prices,
            type='float', digits_compute=dp.get_precision('Account'),
            string='Subtotal', multi='printed',),
        'printed_tax_ids': old_fields.function(
            _printed_prices,
            type='one2many', relation='account.invoice.tax', string='Tax',
            multi='printed'),
        'exempt_amount': old_fields.function(
            _printed_prices, type='float',
            digits_compute=dp.get_precision('Account'),
            string='Exempt Amount', multi='printed'),
        'vat_tax_ids': old_fields.function(
            _printed_prices,
            type='one2many', relation='account.invoice.tax',
            string='VAT Taxes', multi='printed'),
        'vat_amount': old_fields.function(
            _printed_prices, type='float',
            digits_compute=dp.get_precision('Account'),
            string='Vat Amount', multi='printed'),
        'other_taxes_amount': old_fields.function(
            _printed_prices, type='float',
            digits_compute=dp.get_precision('Account'),
            string='Other Taxes Amount', multi='printed')
    }

    available_journals = fields.Many2one(
        'account.journal',
        # compute='_get_available_journal_document_class',
        string='Available Journals')

    journal_document_class_id = fields.Many2one(
        'account.journal.sii_document_class',
        'Documents Type',
        readonly=True,
        store=True,
        states={'draft': [('readonly', False)]})

    # no puedo sacar el compute porque me dice que ya existe la relacion
    available_journal_document_class_ids = fields.Many2many(
        'account.journal.sii_document_class',
        compute='_get_available_journal_document_class',
        string='Available Journal Document Classes')

    turn_issuer = fields.Many2one(
        'partner.activities',
        'Giro Emisor', readonly=True, store=True, required=False,
        states={'draft': [('readonly', False)]},
        default=_set_default_turn_issuer,
        #default=_get_available_issuer_turns
        )

    document_number = fields.Char(
        compute='_get_document_number',
        string='Document Number',
        readonly=True,
    )

    next_invoice_number = fields.Integer(
        related='journal_document_class_id.sequence_id.number_next_actual',
        string='Next Document Number',
        readonly=True)

    use_documents = fields.Boolean(
        related='journal_id.use_documents',
        string='Use Documents?',
        readonly=True)

    sii_document_number = fields.Char(
        string='Document Number',
        copy=False,
        readonly=True, )

    vat_discriminated = fields.Boolean(
        'Discriminate VAT?',
        compute="get_vat_discriminated",
        store=True,
        readonly=False,
        help="Discriminate VAT on Quotations and Sale Orders?")

    supplier_invoice_number = fields.Char(
        copy=False)

    sii_document_class_id = fields.Many2one(
        'sii.document_class',
        related='journal_document_class_id.sii_document_class_id',
        string='Document Type',
        copy=False,
        readonly=True,
        store=True)

    responsability_id = fields.Many2one(
        'sii.responsability',
        string='Responsability',
        related='commercial_partner_id.responsability_id',
        store=True,
    )

    formated_vat = fields.Char(
        string='Responsability',
        related='commercial_partner_id.formated_vat', )

    ####### @api.multi
    ####### def name_get(self):
    #######     TYPES = {
    #######         'out_invoice': _('Invoice'),
    #######         'in_invoice': _('Supplier Invoice'),
    #######         'out_refund': _('Refund'),
    #######         'in_refund': _('Supplier Refund'),
    #######     }
    #######     result = []
    #######     for inv in self:
    #######         result.append(
    #######             (inv.id, "%s %s" % (
    #######                 inv.document_number or TYPES[inv.type], inv.name or '')))
    #######     return result
    #######
    ####### @api.model
    ####### def name_search(self, name, args=None, operator='ilike', limit=100):
    #######     args = args or []
    #######     recs = self.browse()
    #######     if name:
    #######         recs = self.search(
    #######             [('document_number', '=', name)] + args, limit=limit)
    #######     if not recs:
    #######         recs = self.search([('name', operator, name)] + args, limit=limit)
    #######     return recs.name_get()
    # api onchange en lugar de depends.. veamos!
    # @api.onchange('journal_id', 'partner_id', 'turn_issuer','invoice_turn')

    @api.onchange('sii_document_class_id')
    def _check_vat(self):
        boleta_ids = [
            self.env.ref('l10n_cl_invoice.dc_bzf_f_dtn').id,
            self.env.ref('l10n_cl_invoice.dc_b_f_dtm').id]
        if self.sii_document_class_id not in boleta_ids and self.partner_id.document_number == '' or self.partner_id.document_number == '0':
            raise Warning(_("""The customer/supplier does not have a VAT \
defined. The type of invoicing document you selected requires you tu settle \
a VAT."""))


    # @api.one
    @api.depends(
        'sii_document_class_id',
        'sii_document_class_id.document_letter_id',
        'sii_document_class_id.document_letter_id.vat_discriminated',
        'company_id',
        'company_id.invoice_vat_discrimination_default')
    def get_vat_discriminated(self):
        vat_discriminated = False
        # agregarle una condicion: si el giro es afecto a iva, debe seleccionar factura, de lo contrario boleta (to-do)
        if self.sii_document_class_id.document_letter_id.vat_discriminated or self.company_id.invoice_vat_discrimination_default == 'discriminate_default':
            vat_discriminated = True
        self.vat_discriminated = vat_discriminated


    # @api.one
    @api.depends('sii_document_number', 'number')
    def _get_document_number(self):
        if self.sii_document_number and self.sii_document_class_id:
            document_number = (
                self.sii_document_class_id.doc_code_prefix or '') + self.sii_document_number
        else:
            document_number = self.number
        self.document_number = document_number


    # @api.one
    @api.constrains('supplier_invoice_number', 'partner_id', 'company_id')
    def _check_reference(self):
        if self.type in ['out_invoice', 'out_refund'] and self.reference and self.state == 'open':
            domain = [('type', 'in', ('out_invoice', 'out_refund')),
                      # ('reference', '=', self.reference),
                      ('document_number', '=', self.document_number),
                      ('journal_document_class_id.sii_document_class_id', '=',
                       self.journal_document_class_id.sii_document_class_id.id),
                      ('company_id', '=', self.company_id.id),
                      ('id', '!=', self.id)]
            invoice_ids = self.search(domain)
            if invoice_ids:
                raise Warning(
                    _('Supplier Invoice Number must be unique per Supplier and Company!'))

    _sql_constraints = [
        ('number_supplier_invoice_number',
            'unique(supplier_invoice_number, partner_id, company_id)',
         'Supplier Invoice Number must be unique per Supplier and Company!'),
    ]

    @api.onchange('journal_id')
    def re_set_tax_doc(self):
        raise Warning(self.journal_id)

    @api.multi
    def action_number(self):
        obj_sequence = self.env['ir.sequence']

        # We write document_number field with next invoice number by
        # document type
        for obj_inv in self:
            invtype = obj_inv.type
            # if we have a journal_document_class_id is becuse we are in a
            # company that use this function
            # also if it has a reference number we use it (for example when
            # cancelling for modification)
            if obj_inv.journal_document_class_id and not obj_inv.sii_document_number:
                if invtype in ('out_invoice', 'out_refund'):
                    if not obj_inv.journal_document_class_id.sequence_id:
                        raise osv.except_osv(_('Error!'), _(
                            'Please define sequence on the journal related documents to this invoice.'))
                    sii_document_number = obj_sequence.next_by_id(
                        obj_inv.journal_document_class_id.sequence_id.id)
                elif invtype in ('in_invoice', 'in_refund'):
                    sii_document_number = obj_inv.supplier_invoice_number
                obj_inv.write({'sii_document_number': sii_document_number})
                document_class_id = obj_inv.journal_document_class_id.sii_document_class_id.id
                obj_inv.move_id.write(
                    {'document_class_id': document_class_id,
                     'sii_document_number': self.sii_document_number})
        res = super(account_invoice, self).action_number()

        return res
