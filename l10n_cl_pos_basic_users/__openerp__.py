# -*- coding: utf-8 -*-
{   'active': False,
    'author': u'Blanco Martín & Asociados',
    'website': 'http://blancomartin.cl',
    'category': 'Localization/Chile',
    'depends': [
        'l10n_cl_invoice'
        ],
    'description': u'''
\n\nMódulo que simplifica la terminología para usuarios basicos.
Se recomienda instalar sólo en caso de usuarios con poco nivel de conocimiento
contable, y para uso en mesón.
''',
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Chile - Terminología Básica',
    'data': [
        'data/responsability.xml',
        'data/partner.xml',
        'data/sii.document_letter.csv',
        'data/sii.document_class.csv',
    ],
    'version': '0.1',
}
