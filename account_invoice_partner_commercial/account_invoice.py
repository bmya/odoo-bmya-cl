# -*- coding: utf-8 -*-
# {'default_groups_ref': ['base.group_user', 'base.group_partner_manager', 'account.group_account_invoice']}
#['|',('id', 'child_of', user.commercial_partner_id.id),('id','child_of','user.user_id.id')]

from openerp import models, api


class account_invoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def onchange_partner_id(
            self, type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False, company_id=False):
        ret = super(account_invoice, self).onchange_partner_id(
            type=type, partner_id=partner_id, date_invoice=date_invoice,
            payment_term=payment_term, partner_bank_id=partner_bank_id,
            company_id=company_id)
        if 'value' not in ret:
            ret['value'] = {}
        if partner_id:
            # Brings selected partner record
            partner = self.env['res.partner'].browse(partner_id)
            # If there is no partner record selected, brings company id
            
            ret['value']['user_id'] = partner.user_id.id or self.env.uid
        else:
            ret['value']['user_id'] = self.env.uid
        return ret
