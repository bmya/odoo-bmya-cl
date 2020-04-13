from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_cl_partner_activities_ids = fields.Many2many(
        'l10n_cl.company.activities', string='Activities Names',
        help='Please select the economic activities from SII\'s nomenclator')
    l10n_cl_available_partner_activities_ids = fields.Many2many(
        'l10n_cl.company.activities', compute='_compute_available_activities')

    @api.onchange('l10n_cl_partner_activities_ids')
    def _select_activity_description_from_codes(self):
        if len(self.l10n_cl_partner_activities_ids) > 0 and not self.l10n_cl_activity_description:
            self.l10n_cl_activity_description = self.l10n_cl_partner_activities_ids[0].name

    @api.depends('l10n_cl_sii_taxpayer_type')
    def _compute_available_activities(self):
        self.l10n_cl_available_partner_activities_ids = False
        for rec in self.filtered(lambda x: x.l10n_cl_sii_taxpayer_type):
            rec.l10n_cl_available_partner_activities_ids = self.env['l10n_cl.company.activities'].search(
                [('tax_category', 'in', ['nd', rec.l10n_cl_sii_taxpayer_type])]).ids
