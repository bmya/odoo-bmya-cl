# -*- coding: utf-8 -*-
{
    'name': 'Chile - Localization Installation Wizard',
    'version': '10.0.0.1',
    'category': 'Chilean Localization',
    'license': 'AGPL-3',
    'sequence': 14,
    'summary': 'Localization, Chile, Configuration',
    'description': """Helps and make you easiest to install
several options for chilean localization. You can see in a
single screen, the progress of what is not fully developed yet.
    """,
    'author':  u'Blanco Martín & Asociados',
    'website': 'http://blancomartin.cl',
    'depends': [
        'base_setup'
    ],
    'data': [
        'l10n_cl_base_groups.xml',
        'res_config_view.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': True,
}

