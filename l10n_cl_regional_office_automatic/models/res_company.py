from odoo import api, fields, models

L10N_CL_SII_REGIONAL_OFFICES_ITEMS = [
    ('ur_Anc', 'Ancud'),
    ('ur_Ang', 'Angol'),
    ('ur_Ant', 'Antofagasta'),
    ('ur_Ari', 'Arica y Parinacota'),
    ('ur_Ays', 'Aysén'),
    ('ur_Cal', 'Calama'),
    ('ur_Cas', 'Castro'),
    ('ur_Cau', 'Cauquenes'),
    ('ur_Cha', 'Chaitén'),
    ('ur_Chn', 'Chañaral'),
    ('ur_ChC', 'Chile Chico'),
    ('ur_Chi', 'Chillán'),
    ('ur_Coc', 'Cochrane'),
    ('ur_Cop', 'Concepción '),
    ('ur_Cos', 'Constitución'),
    ('ur_Coo', 'Copiapo'),
    ('ur_Coq', 'Coquimbo'),
    ('ur_Coy', 'Coyhaique'),
    ('ur_Cur', 'Curicó'),
    ('ur_Ill', 'Illapel'),
    ('ur_Iqu', 'Iquique'),
    ('ur_LaF', 'La Florida'),
    ('ur_LaL', 'La Ligua'),
    ('ur_LaS', 'La Serena'),
    ('ur_LaU', 'La Unión'),
    ('ur_Lan', 'Lanco'),
    ('ur_Leb', 'Lebu'),
    ('ur_Lin', 'Linares'),
    ('ur_Lod', 'Los Andes'),
    ('ur_Log', 'Los Ángeles'),
    ('ur_Oso', 'Osorno'),
    ('ur_Ova', 'Ovalle'),
    ('ur_Pan', 'Panguipulli'),
    ('ur_Par', 'Parral'),
    ('ur_Pic', 'Pichilemu'),
    ('ur_Por', 'Porvenir'),
    ('ur_PuM', 'Puerto Montt'),
    ('ur_PuN', 'Puerto Natales'),
    ('ur_PuV', 'Puerto Varas'),
    ('ur_PuA', 'Punta Arenas'),
    ('ur_Qui', 'Quillota'),
    ('ur_Ran', 'Rancagua'),
    ('ur_SaA', 'San Antonio'),
    ('ur_Sar', 'San Carlos'),
    ('ur_SaF', 'San Felipe'),
    ('ur_SaD', 'San Fernando'),
    ('ur_SaV', 'San Vicente de Tagua Tagua'),
    ('ur_SaZ', 'Santa Cruz'),
    ('ur_SaC', 'Santiago Centro'),
    ('ur_SaN', 'Santiago Norte'),
    ('ur_SaO', 'Santiago Oriente'),
    ('ur_SaP', 'Santiago Poniente'),
    ('ur_SaS', 'Santiago Sur'),
    ('ur_TaT', 'Tal-Tal'),
    ('ur_Tac', 'Talca'),
    ('ur_Tah', 'Talcahuano'),
    ('ur_Tem', 'Temuco'),
    ('ur_Toc', 'Tocopilla'),
    ('ur_Vld', 'Valdivia'),
    ('ur_Val', 'Vallenar'),
    ('ur_Vlp', 'Valparaíso'),
    ('ur_Vic', 'Victoria'),
    ('ur_ViA', 'Villa Alemana'),
    ('ur_ViR', 'Villarrica'),
    ('ur_ViM', 'Viña del Mar'),
]

class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_cl_sii_regional_office = fields.Selection(
        L10N_CL_SII_REGIONAL_OFFICES_ITEMS, related='partner_id.l10n_cl_sii_regional_office',
        translate=False, string='SII Regional Office')

    @api.onchange('city_id')
    @api.depends('city_id')
    def _change_regional_office(self):
        if self.country_id != self.env.ref('base.cl'):
            return
        # self.sudo().l10n_cl_sii_regional_office = self.city_id.l10n_cl_sii_regional_office
        self.partner_id.sudo().l10n_cl_sii_regional_office = self.city_id.l10n_cl_sii_regional_office
