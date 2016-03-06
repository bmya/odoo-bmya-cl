# -*- coding: utf-8 -*-
import openerp
from openerp.osv import osv
from openerp import tools
import os
from openerp.tools.image import image_resize_image
from openerp import models, api


class res_company(osv.osv):
    _inherit="res.company"
    _name="res.company"
    
    def init(self, cr):
        img=open(os.path.join(os.path.dirname(__file__), 'static', 'src', 'img','company_logo.png'), 'rb') .read().encode('base64')
        cr.execute("UPDATE res_partner SET image=%s WHERE name = 'Your Company'", (img,))
        cr.execute("UPDATE res_partner SET image=%s WHERE name = 'Blanco Martín EIRL'", (img,))
        size = (180, None)
        cr.execute('UPDATE res_company SET logo_web=%s', (image_resize_image(img, size),))


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def create(self, vals):
        inherit_id = vals.get('inherit_id', False)
        if inherit_id:
            # this is an inheritance
            del vals['inherit_id']
            super(ResCompany, self.browse(inherit_id)).write(vals)
            return self
        return super(ResCompany, self).create(vals)
