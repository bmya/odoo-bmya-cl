# -*- coding: utf-8 -*-
# from __future__ import print_function
from odoo import models, fields, api
from datetime import datetime
from odoo.tools.translate import _
from odoo.exceptions import Warning as UserError
import logging
_logger = logging.getLogger(__name__)


class PickingLineDescription(models.Model):
    _inherit = 'stock.move'

    move_description = fields.Char('Motivo del Movimiento')


# class StockPackOperation(models.Model):
#     _inherit = 'stock.pack.operation'
#
#     move_description = fields.Char('Motivo del Movimiento')
