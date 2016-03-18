# -*- coding: utf-8 -*-
from __future__ import print_function
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import logging


_logger = logging.getLogger(__name__)

class account_journal_document_config(osv.osv_memory):

    _name = 'account.journal.document_config'

    _columns = {
        'debit_notes': fields.selection(
            [('dont_use','Do not use'), ('own_sequence','Use')],
            string='Debit Notes', required=True,),
        'credit_notes': fields.selection(
            [('own_sequence','Use')], string='Credit Notes', required=True,),
        'dte_register': fields.boolean(
            'Register Electronic Documents?', default=True),
        'non_dte_register': fields.boolean(
            'Register Manual Documents?'),
        'free_tax_zone': fields.boolean(
            'Register Free-Tax Zone or # 1057 Resolution Documents?'),
        'settlement_invoice': fields.boolean(
            'Register Settlement Invoices?'),
        'weird_documents': fields.boolean(
            'Weird Documents', help='Include weird invoices as ...'),
        'excempt_documents': fields.boolean('VAT Excempt Invoices'),
    }

    _defaults= {
        'debit_notes': 'own_sequence',
        'credit_notes': 'own_sequence',
    }

    def confirm(self, cr, uid, ids, context=None):
        """
        Confirm Configure button
        """
        if context is None:
            context = {}

        journal_ids = context.get('active_ids', False)
        wizard = self.browse(cr, uid, ids[0], context=context)
        self.create_journals(cr, uid, journal_ids, wizard, context=context)

    def create_journals(self, cr, uid, journal_ids, wz, context=None):
        for journal in self.pool['account.journal'].browse(
                cr, uid, journal_ids, context=context):
            responsability = journal.company_id.responsability_id
            if not responsability.id:
                raise orm.except_orm(
                    _('Your company has not setted any responsability'),
                    _('Please, set your company responsability in the company partner before continue.'))
                _logger.warning(
                    'Your company "%s" has not setted any responsability.' % journal.company_id.name)
          
            journal_type = journal.type
            if journal_type in ['sale', 'sale_refund']:
                letter_ids = [x.id for x in responsability.issued_letter_ids]
            elif journal_type in ['purchase', 'purchase_refund']:
                letter_ids = [x.id for x in responsability.received_letter_ids]
            
            if journal_type == 'sale':
                for doc_type in ['invoice', 'debit_note']:
                    self.create_journal_document(
                        cr, uid, letter_ids, doc_type, journal.id, wz, context)
            elif journal_type == 'purchase':
                for doc_type in ['invoice', 'debit_note', 'invoice_in']:
                    self.create_journal_document(
                        cr, uid, letter_ids, doc_type, journal.id, wz, context)
                    #self.create_journal_document(cr, uid, letter_ids, doc_type, journal.id, non_dte_register, dte_register, settlement_invoice, free_tax_zone, credit_notes, debit_notes, context)
            elif journal_type in ['sale_refund', 'purchase_refund']:
                self.create_journal_document(
                    cr, uid, letter_ids, 'credit_note', journal.id, wz, context)

    def create_sequence(self, cr, uid, name, journal, context=None):
        vals = {
            'name': journal.name + ' - ' + name,
            'padding': 6,
            'prefix': journal.point_of_sale,
        }
        sequence_id = self.pool['ir.sequence'].create(
            cr, uid, vals, context=context)
        return sequence_id

    def create_journal_document(self, cr, uid, letter_ids, document_type,
                                journal_id, wz, context=None):

        if_zf = [] if wz.free_tax_zone else [901, 906, 907]
        if_lf = [] if wz.settlement_invoice else [40, 43]
        if_tr = [] if wz.weird_documents else [29, 108, 914, 911, 904, 905]
        # if_pr = [] if wz.purchase_invoices else [45, 46]
        if_na = [] if wz.excempt_documents else [32, 34]
        dt_types_exclude = if_zf + if_lf + if_tr + if_na
        print(dt_types_exclude)

        document_class_obj = self.pool['sii.document_class']
        document_class_ids = document_class_obj.search(
            cr, uid, [
                ('document_letter_id', 'in', letter_ids),
                ('document_type', '=', document_type),
                ('sii_code', 'not in', dt_types_exclude)], context=context)


        # ('sii_code', 'not in', dt_types_exclude)
        journal_document_obj = self.pool['account.journal.sii_document_class']
        journal = self.pool['account.journal'].browse(
            cr, uid, journal_id, context=context)
        sequence = 10

        for document_class in document_class_obj.browse(
                cr, uid, document_class_ids, context=context):
            print('ws existente -- non_dte_register: %s settlement_invoice: %s free_tax: %s, dte_register %s' % (wz.non_dte_register, wz.settlement_invoice, wz.free_tax_zone, wz.dte_register))
            print(document_class.report_name, document_class.sii_code)
            if not document_class.dte:
                print('documento manual: ')
                if wz.non_dte_register:
                    print('non dte')
                else:
                    continue
            else:
                print('documento electronico')
                if wz.dte_register:
                    print('dte')
                    pass
                else:
                    continue

            print('crear')
            sequence_id = self.create_sequence(cr, uid, document_class.name,
                                               journal, context)
            vals = {
                'sii_document_class_id': document_class.id,
                'sequence_id': sequence_id,
                'journal_id': journal.id,
                'sequence': sequence,
            }
            journal_document_obj.create(cr, uid, vals, context=context)
            sequence +=10
