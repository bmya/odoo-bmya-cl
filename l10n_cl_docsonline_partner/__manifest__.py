# -*- coding: utf-8 -*-
{
    "name": """Chile get customer data from www.documentosonline.cl""",
    'version': '11.0.1.0.0',
    'category': 'Localization/Chile',
    'sequence': 12,
    'author':  'Blanco Martín & Asociados',
    'website': 'http://blancomartin.cl',
    'license': 'AGPL-3',
    'summary': '',
    'depends': [
        'l10n_cl_edi',
    ],
    'data': [
        'views/partner_view.xml',
        'data/ir.config_parameter.xml',
        'wizard/data_docsonline_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
