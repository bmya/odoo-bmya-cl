{
    "name": """Chile - Activities for Partners""",
    'version': '1.0.',
    'category': 'Localization/Chile',
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
        'l10n_cl',
    ],
    'data': [
        'views/partner_activities_view.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
