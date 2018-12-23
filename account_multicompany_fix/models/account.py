# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountNameGet(models.AbstractModel):
    _name = 'account.name.get'


class AccountAccount(models.Model):
    _name = 'account.account'
    _inherit = ['account.account', 'account.name.get']

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.company_id.name:
                name = '%s (%s)' % (name, record.company_id.name)
            result.append((record.id, name))
        return result


class AccountJournal(models.Model):
    _name = 'account.journal'
    _inherit = ['account.journal', 'account.name.get']

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.company_id.name:
                name = '%s (%s)' % (name, record.company_id.name)
            result.append((record.id, name))
        return result


class AccountTax(models.Model):
    _name = 'account.tax'
    _inherit = ['account.tax', 'account.name.get']

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.company_id.name:
                name = '%s (%s)' % (name, record.company_id.name)
            result.append((record.id, name))
        return result


class AccountFiscalPosition(models.Model):
    _name = 'account.fiscal.position'
    _inherit = ['account.fiscal.position', 'account.name.get']

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.company_id.name:
                name = '%s (%s)' % (name, record.company_id.name)
            result.append((record.id, name))
        return result
