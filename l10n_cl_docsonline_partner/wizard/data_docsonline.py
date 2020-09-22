from odoo import api, fields, models


class PartnerDocumentsOnline(models.TransientModel):
    """Wizard to show www.documentosonline.cl data"""
    _name = 'res.partner.docs.online'
    _description = 'www.documentosonline.cl wizard'

    partner_id = fields.Many2one('res.partner')
    name = fields.Char(string='Name', related='partner_id.name', readonly=True)
    docs_online_data_ids = fields.Many2many('res.partner.docs.online.data', string='-')

    @api.model
    def truncate(self):
        cursor = self.env.cr
        cursor.execute('truncate res_partner_docs_online cascade')

    def pick_partner(self):
        # implemented just for one record by now
        nr = self.docs_online_data_ids[0]
        self.partner_id.update({
            'name': nr.name,
            'street': nr.street,
            'street2': nr.street2,
            'city': nr.city,
            'city_id': nr.city_id,
            'state_id': nr.state_id,
            'l10n_cl_dte_email': nr.l10n_cl_dte_email,
            'vat': nr.vat,
            'l10n_cl_activity_description':  nr.l10n_cl_activity_description,
            'country_id':  nr.country_id,
            'l10n_cl_sii_taxpayer_type':  '1',  # nr.l10n_cl_sii_taxpayer_type,
            'type':  nr.type,
            'l10n_latam_identification_type_id': self.env.ref('l10n_cl.it_RUT').id
        })
        self.partner_id.press_to_update()

    def pick_partner_protect(self):
        # implemented just for one record by now
        nr = self.docs_online_data_ids[0]
        self.partner_id.update({
            'city': nr.city,
            'city_id': nr.city_id,
            'state_id': nr.state_id,
            'l10n_cl_dte_email': nr.l10n_cl_dte_email,
            'vat': nr.vat,
            'l10n_cl_activity_description':  nr.l10n_cl_activity_description,
            'country_id':  nr.country_id,
            'l10n_cl_sii_taxpayer_type':  '1',  # nr.l10n_cl_sii_taxpayer_type,
            'type':  nr.type,
            'l10n_latam_identification_type_id': self.env.ref('l10n_cl.it_RUT').id
        })


class PartnerDocumentsOnLineData(models.TransientModel):
    _name = 'res.partner.docs.online.data'
    _description = 'www.documentosonline.cl wizard #2'

    partner_docs_ids = fields.Many2many('res.partner.docs.online', string='Lines')
    name = fields.Char('Name')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    city = fields.Char('City')
    city_id = fields.Many2one('res.city', 'County')
    state_id = fields.Many2one('res.country.state', string='Province')
    l10n_cl_dte_email = fields.Char('DTE Email')
    vat = fields.Char('RUT')
    l10n_cl_activity_description = fields.Char(string='Activity Description')
    country_id = fields.Many2one('res.country', string='Country')
    l10n_cl_sii_taxpayer_type = fields.Selection(
        [('1', 'VAT Affected (1st Category)'), ('2', 'Fees Receipt Issuer (2nd category)'), ('3', 'End Consumer'),
         ('4', 'Foreigner')], 'Taxpayer Type', index=True)
    type = fields.Selection([('contact', 'Contact'), ('invoice', 'Invoice Address'), ('delivery', 'Shipping Address'),
            ('other', 'Other Address'), ('private', 'Private Address')], string='Type of Address')

    @api.model
    def truncate(self):
        cursor = self.env.cr
        cursor.execute('truncate res_partner_docs_online_data cascade')

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.vat:
                name = '%s %s' % (name, record.vat)
            if record.street:
                name = '%s %s' % (name, record.street)
            if record.street2:
                name = '%s %s' % (name, record.street2)
            if record.city:
                name = '%s, %s' % (name, record.city)
            if record.type:
                if record.type == 'other':
                    name = '%s (%s)' % (name, 'Sucursal')
            if record.l10n_cl_activity_description:
                name = '%s - %s' % (name, record.l10n_cl_activity_description)
            result.append((record.id, name))
        return result
