# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import Warning

try:
    import xmltodict
except ImportError:
    pass

try:
    import base64
except ImportError:
    pass



class caf(models.Model):
    _name = 'dte.caf'

    name = fields.Char('File Name', readonly=True, compute='_get_filename')

    filename = fields.Char('File Name')

    caf_file = fields.Binary(
        string='CAF XML File', filters='*.xml', required=True,
        store=True, help='Upload the CAF XML File in this holder')

    _sql_constraints=[(
        'filename_unique','unique(filename)','Error! Filename Already Exist!')]
        
    issued_date = fields.Date('Issued Date')
    
    sii_document_class = fields.Integer('SII Document Class')

    start_nm = fields.Integer(
        string='Start Number', help='CAF Starts from this number')
    
    final_nm = fields.Integer(
        string='End Number', help='CAF Ends to this number')

    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_use', 'In Use'),
        ('spent', 'Spent'),
        ('cancelled', 'Cancelled')], string='Status',
        default='draft', help='''Draft: means it has not been used yet.
You must put in in used in order to make it available for use. Spent: means
that the number interval has been exhausted. Cancelled means it has been
deprecated by hand.''')

    rut_n = fields.Char(string='RUT')

    company_id = fields.Many2one(
        'res.company', 'Company', required=False,
        default=lambda self: self.env.user.company_id)

    sequence_id = fields.Many2one(
        'ir.sequence', 'Sequence', required=False)

    use_level = fields.Float(string="Use Level", compute='_use_level')

    @api.depends('start_nm', 'final_nm', 'sequence_id', 'status')
    def _use_level(self):
        for r in self:
            if r.status not in ['draft','cancelled']:
                try:            
                    r.use_level = 100 * (
                        float(r.sequence_id.number_next_actual - 1) / float(
                            r.final_nm - r.start_nm + 1))
                except ZeroDivisionError:
                    r.use_level = 0
                print(r.use_level, r.sequence_id.number_next_actual,
                      r.final_nm, r.start_nm)
                if r.sequence_id.number_next_actual > r.final_nm \
                    and r.status == 'in_use':
                    #r.status = 'spent'
                    self.env.cr.execute("""UPDATE dte_caf SET status = 'spent' \
WHERE filename = '%s'""" % r.filename)
                    print 'spent'
                elif r.sequence_id.number_next_actual <= r.final_nm \
                    and r.status == 'spent':
                    #r.status = 'in_use'
                    self.env.cr.execute("""UPDATE dte_caf SET status \
= 'in_use' WHERE filename = '%s'""" % r.filename)
                    print 'in_use'
                
            else:
                r.use_level = 0



    @api.one
    def action_enable(self):
        result = xmltodict.parse(
            base64.b64decode(self.caf_file).replace(
                '<?xml version="1.0"?>','',1))['AUTORIZACION']['CAF']['DA']

        self.start_nm = result['RNG']['D']
        self.final_nm = result['RNG']['H']
        self.sii_document_class = result['TD']
        self.issued_date = result['FA']
        self.rut_n = 'CL' + result['RE'].replace('-','')
        if not self.sequence_id:
            raise Warning(_(
                'You should select a DTE sequence before enabling this \
CAF record'))
        elif self.rut_n != self.company_id.vat:
            raise Warning(_(
                'Company vat %s should be the same that assigned company\'s \
vat: %s!') % (self.rut_n, self.company_id.vat))
        elif self.sii_document_class != self.sequence_id.sii_document_class:
            raise Warning(_(
                '''SII Document Type for this CAF is %s and selected sequence \
associated document class is %s. This values should be equal for DTE Invoicing \
to work properly!''') % (
                self.sii_document_class, self.sequence_id.sii_document_class))
        elif self.sequence_id.number_next_actual < self.start_nm \
                or self.sequence_id.number_next_actual > self.final_nm:
            raise Warning(_(
                'Folio Number %s should be between %s and %s CAF \
Authorization Interval!') % (
                self.sequence_id.number_next_actual, self.start_nm,
                self.final_nm))
        else:
            self.status = 'in_use'

    @api.one
    def action_cancel(self):
        self.status = 'cancelled'

    @api.one
    def _get_filename(self):
        self.name = self.filename


class sequence_caf(models.Model):
    _inherit = "ir.sequence"
    
    sii_document_class = fields.Integer(
        'SII Code', readonly=True, compute='_get_sii_document_class')

    is_dte = fields.Boolean('IS DTE?', readonly=True, compute='_check_dte')
    
    dte_caf_ids = fields.One2many(
        'dte.caf', 'sequence_id', 'DTE Caf')

    @api.one
    def _get_sii_document_class(self):
        r = self
        obj = r.env['account.journal.sii_document_class'].search(
            [('sequence_id', '=', r.id)])
        r.sii_document_class = obj.sii_document_class_id.sii_code
        

    @api.one
    def _check_dte(self):
        r = self
        obj = r.env['account.journal.sii_document_class'].search(
            [('sequence_id', '=', r.id)])
        r.is_dte = obj.sii_document_class_id.dte \
                   and obj.sii_document_class_id.document_type in [
            'invoice', 'debit_note', 'credit_note', 'stock_picking',
            'stock_voucher']
