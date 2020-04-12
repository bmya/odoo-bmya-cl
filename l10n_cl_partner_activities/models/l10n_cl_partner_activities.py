from odoo import api, fields, models


class PartnerActivities(models.Model):
    _description = 'SII Economical Activities'
    _name = 'l10n_cl.partner.activities'

    code = fields.Char('Activity Code', required=True)
    parent_id = fields.Many2one('l10n_cl.partner.activities', 'Parent Activity', ondelete='cascade')
    grand_parent_id = fields.Many2one('l10n_cl.partner.activities', related='parent_id.parent_id',
                                      string='Grand Parent Activity', ondelete='cascade', store=True)
    name = fields.Char('Complete Name', required=True)
    vat_affected = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
        ('nd', 'ND')
    ], 'VAT Affected', default='yes')
    tax_category = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('nd', 'ND')
    ], 'TAX Category', default='1')
    internet_available = fields.Boolean('Available at Internet', default=True)
    active = fields.Boolean('Active', help="Allows you to hide the activity without removing it.", default=True)
    partner_ids = fields.Many2many('res.partner', id1='activities_id', id2='partner_id', string='Partners')

    @api.model
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.code:
                name = '(%s) %s' % (record.code, name)
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if self._context.get('search_by_code', False):
            if name:
                args = args if args else []
                args.extend(['|', ['name', 'ilike', name], ['code', 'ilike', name]])
                name = ''
        return super(PartnerActivities, self).name_search(name=name, args=args, operator=operator, limit=limit)
