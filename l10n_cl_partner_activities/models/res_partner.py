from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_cl_dte_email = fields.Char('DTE Email')
    l10n_cl_partner_activities_ids = fields.Many2many(
        'l10n_cl.partner.activities', id1='partner_id', id2='activities_id', string='Activities Names',
        help='Please select the economic activities from SII\'s nomenclator',
        domain=lambda self: [('id', 'in', self._compute_available_activities())]
    )
    l10n_cl_activity_description = fields.Char(string='Activity Description')
    l10n_cl_activities_opt = fields.Selection([
        ('encoded_activity', 'Business Turn Based on Economic Activities (B2B or SMEs)'),
        ('activity_description', 'Business Turn Based on Activity Description (B2C or MSEs)'),
    ], related='company_id.l10n_cl_activities_opt', readonly=True, help="""If your company is a small or medium 
    business, probably you'd prefer to describe your activity or your partner's activities based on the SII's 
    economic activities nomenclator.
    But if your company is a micro or small enterprise, or if you mostly serves your customers at a counter, 
    you will probably prefer to describe your partners' activities based on a simple description through a phrase. 
    In either case, establishing at least one of the economic activities for your own company is mandatory.""")

    def _compute_available_activities(self):
        records = self.env['l10n_cl.partner.activities'].search([]).filtered(lambda r: len(r.code) >= 6).ids
        return records

    @api.onchange('l10n_cl_partner_activities_ids')
    def _select_activity_description_from_codes(self):
        if len(self.l10n_cl_partner_activities_ids) > 0:
            self.l10n_cl_activity_description = self.l10n_cl_partner_activities_ids[0].name

    # def write(self, values):
    #     for record in self:
    #         if values.get('l10n_cl_partner_activities_ids') and record.l10n_cl_activities_opt == 'encoded_activity' \
    #                 and not record.l10n_cl_activity_description:
    #             values['l10n_cl_activity_description'] = self.env['l10n_cl.partner.activities'].browse(
    #                 values['l10n_cl_partner_activities_ids'])[0].name
    #     return super().write(values)
