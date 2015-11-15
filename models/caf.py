# -*- coding: utf-8 -*-
from openerp import models, fields, api
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
    
    sii_code = fields.Integer('SII Document Code')

    start_nm = fields.Integer(
        string='Start Number', help='CAF Starts from this number')
    
    final_nm = fields.Integer(
        string='End Number', help='CAF Ends to this number')

    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_use', 'In Use'),
        ('spent', 'Spent'),
        ('cancelled', 'Cancelled')], string='Status', default='draft',
        help='''Draft:  means it has not been used yet. You must put in in used
in order to make it available for use. Spent: means that the number interval
has been exhausted. Cancelled means it has been deprecated by hand.''')

    rut_n = fields.Char(string='RUT')

    company_id = fields.Many2one(
        'res.company', 'Company', required=False,
        default=lambda self: self.env.user.company_id)

    # dte_id = fields.Many2one(
    #     
    #     '')

    @api.one
    def action_enable(self):
        result = xmltodict.parse(
            base64.b64decode(self.caf_file).replace(
                '<?xml version="1.0"?>','',1))['AUTORIZACION']['CAF']['DA']

        self.start_nm = result['RNG']['D']
        self.final_nm = result['RNG']['H']
        self.sii_code = result['TD']
        self.issued_date = result['FA']
        self.rut_n = 'CL' + result['RE'].replace('-','')
        # validar si el RUT del CAF es igual al RUT de la compañia 
        # seleccionada
        self.status = 'in_use'

    @api.one
    def action_cancel(self):
        self.status = 'cancelled'

    @api.one
    def _get_filename(self):
        self.name = self.filename
