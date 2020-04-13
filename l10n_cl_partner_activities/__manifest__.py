{
    "name": """Chile - Activities for Partners""",
    'version': '1.0.',
    'category': 'Localization/Chile',
    "license": "LGPL-3",
    'sequence': 12,
    'author':  'Blanco Martín & Asociados',
    'description': """
Agrega Código de Actividad a los partners
=========================================
Este codigo recupera una funcionalidad de versiones anteriores, que permite utilizar los códigos de actividad económica
en los partners.
    """,
    'website': 'http://blancomartin.cl',
    'depends': [
        'l10n_cl_edi',
    ],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
