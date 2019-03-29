# -*- coding: utf-8 -*-
# from __future__ import print_function
from openerp import models, fields, api
from datetime import datetime
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError
import logging
_logger = logging.getLogger(__name__)

try:
    import xlrd
    from xlrd.sheet import ctype_text
except ImportError:
    pass

try:
    import base64
except ImportError:
    pass


class StockMove(models.Model):
    _inherit = 'stock.picking'

    move_record_id = fields.Many2one(
        'stock.xls.move', 'Move Record File', index=True, ondelete='restrict')
    product_uom_qty = fields.Float("Quantity On Hand")
    filename = fields.Char('File Name')
    move_file = fields.Binary(
        string='Move Records File', filters='*.xls', required=False,
        readonly=True, track_visibility='onchange',
        states={'draft': [('readonly', False)]},
        store=True, help='Upload the XLS Move File in this holder')

    def get_product_from_sku(self, sku):
        """
        Method to obtain the product object from its default_code (sku)
        @author: Daniel Blanco <daniel[at]blancomartin.cl>
        """
        prod_obj = self.env['product.product']
        prod_id = prod_obj.search(['|', ('default_code', '=ilike', sku), ('barcode', '=ilike', sku)])
        if len(prod_id) == 1:
            return prod_id
        elif len(prod_id) > 1:
            return prod_id[0]
        else:
            raise UserError('No product found for this SKU: %s' % sku)

    def read_excel(self, xls_file):
        filecontent = base64.b64decode(xls_file)
        xl_workbook = xlrd.open_workbook(
            file_contents=filecontent, encoding_override='cp1252')
        xl_sheet = xl_workbook.sheet_by_index(0)
        row = xl_sheet.row(0)
        datos_title = []
        for idx, cell_obj in enumerate(row):
            datos_title.append(cell_obj.value)
        title_available = ['SKU', 'NAME', 'DESCRIPTION', 'QTY']
        if datos_title != title_available:
            raise UserError(_(
                'XLS Titles {} Do not match with the correct format. \
Should be: {}'.format(datos_title, title_available)))
        num_cols = xl_sheet.ncols
        excel_lines = [(5, )]
        for row_idx in range(0, xl_sheet.nrows):
            row_data = {}
            if row_idx == 0:
                continue
            for col_idx in range(0, num_cols):
                cell_obj = xl_sheet.cell(row_idx, col_idx)
                try:
                    row_data[datos_title[col_idx]] = cell_obj.value
                except:
                    raise UserError('could not copy %s - %s' % (col_idx, cell_obj.value))
            product_id = self.get_product_from_sku(row_data['SKU'])
            excel_line = {
                'product_id': product_id.id,
                'name': product_id.product_tmpl_id.name,
                'move_description': row_data['DESCRIPTION'],
                'product_uom_qty': float(row_data['QTY']),  # added to try to bypass serial number
                'reserver_availability': float(row_data['QTY']),  # added to try to bypass serial number
                'quantity_done': float(row_data['QTY']),
                'product_uom': product_id.uom_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
                'date_expected': datetime.now(),
                'state': 'draft',
            }
            excel_lines.append((0, 0, excel_line))

        return excel_lines

    @api.onchange('move_file')
    def _compute_lines(self):
        if self.move_file and self.picking_type_code == "internal":
            move_lines = self.read_excel(self.move_file)
            self.move_lines = move_lines
