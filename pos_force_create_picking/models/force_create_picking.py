# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError
import logging
_logger = logging.getLogger(__name__)
# python force_create_picking
# este codigo crea el picking para las siguientes condiciones
#	- picking_id vacio, y
# 	- estado facturado
# objeto que hay que heredar: pos.order
# funcion que hay que ejecutar
# point_of_sale.pos_order.create_picking()
# ver si va el pos_order o anda solo. creo que no hace falta
# porque hereda a ese objeto, y en ese objeto ya está la clase
'''
Clase que hereda el pos.order
@autor: Daniel Blanco daniel[at]blancomartin.cl
@version: 2016-08-19
'''
class pos_order(models.Model):
    _inherit="pos.order"
    _description="Force the picking to be created"

    @api.model
    def create_picking_new(self, po):
        """Create a picking for each order and validate it."""
        picking_obj = self.env['stock.picking']
        partner_obj = self.env['res.partner']
        move_obj = self.env['stock.move']
        order = po
        if all(t == 'service' for t in order.lines.mapped('product_id.type')):
            _logger.info('no hay productos almacenables y consumibles en la venta')
            return
        raise UserError('fucking!')
        # addr = order.partner_id and partner_obj.address_get(self._cr, self._uid, [order.partner_id.id], ['delivery']) or {}
        addr = order.partner_id and partner_obj.address_get(
            self._cr, self.uid, ids=[order.partner_id.id], adr_pref=['delivery']) or {}
        # address_get(self, cr, uid, ids, adr_pref=None, context=None):

        raise UserError('fuck1 addr {}'.format(addr))
        picking_type = order.picking_type_id
        picking_id = False
        if picking_type:
            picking_id = picking_obj.create(cr, uid, {
                'origin': order.name,
                'partner_id': addr.get('delivery',False),
                'date_done' : order.date_order,
                'picking_type_id': picking_type.id,
                'company_id': order.company_id.id,
                'move_type': 'direct',
                'note': order.note or "",
                'invoice_state': 'none',
            }, context=context)
            self.write(cr, uid, [order.id], {'picking_id': picking_id}, context=context)
        location_id = order.location_id.id
        if order.partner_id:
            destination_id = order.partner_id.property_stock_customer.id
        elif picking_type:
            if not picking_type.default_location_dest_id:
                raise osv.except_osv(_('Error!'), _('Missing source or destination location for picking type %s. Please configure those fields and try again.' % (picking_type.name,)))
            destination_id = picking_type.default_location_dest_id.id
        else:
            destination_id = partner_obj.default_get(cr, uid, ['property_stock_customer'], context=context)['property_stock_customer']

        move_list = []
        for line in order.lines:
            if line.product_id and line.product_id.type == 'service':
                continue

            move_list.append(move_obj.create(cr, uid, {
                'name': line.name,
                'product_uom': line.product_id.uom_id.id,
                'product_uos': line.product_id.uom_id.id,
                'picking_id': picking_id,
                'picking_type_id': picking_type.id,
                'product_id': line.product_id.id,
                'product_uos_qty': abs(line.qty),
                'product_uom_qty': abs(line.qty),
                'state': 'draft',
                'location_id': location_id if line.qty >= 0 else destination_id,
                'location_dest_id': destination_id if line.qty >= 0 else location_id,
            }, context=context))

        if picking_id:
            picking_obj.action_confirm(cr, uid, [picking_id], context=context)
            picking_obj.force_assign(cr, uid, [picking_id], context=context)
            picking_obj.action_done(cr, uid, [picking_id], context=context)
        elif move_list:
            move_obj.action_confirm(cr, uid, move_list, context=context)
            move_obj.force_assign(cr, uid, move_list, context=context)
            move_obj.action_done(cr, uid, move_list, context=context)
        return True


    '''
    Funcion para forzar la creacion del picking
    @autor: Daniel Blanco daniel[at]blancomartin.cl
    @version: 2016-08-19
    '''
    #"@api.model
    @api.multi
    def force_create_picking(self):
        for po in self:
            if po.picking_id.id == 0:
                _logger.info('Order: {}, picking DOES NOT EXIST'.format(po.name))
                if 1==1: #try:
                    _logger.info(
                        'antes de hacer')
                    self.create_picking_new(po)
                    _logger.info(
                        'despes de hacer')
                else: #except:
                    _logger.info('Order: {}, picking COULD NOT BEEN CREATED'.format(po.name))
            else:
                pass
                _logger.info('Order: {}, picking {} is OK'.format(po.name, po.picking_id.name))


    picking_id_id = fields.Integer('Picking ID',
                                   compute='_get_picking_id')

    @api.multi
    @api.depends('picking_id')
    def _get_picking_id(self):
        # self.ensure_one()
        for po in self:
            if all(t == 'service' for t in po.lines.mapped('product_id.type')):
                _logger.info('no hay productos almacenables y consumibles en la venta')
                po.picking_id_id = 99999999
            else:
                po.picking_id_id = po.picking_id.id
