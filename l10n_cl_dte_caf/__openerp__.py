# -*- coding: utf-8 -*-
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
{
    'author': u'Blanco Martín & Asociados',
    'category': 'Localization/Chile',
    'depends': ['l10n_cl_invoice', 'user_signature_key'],
    "external_dependencies": {
        'python': [
            'xmltodict',
            'base64'
        ]
    },
    'description': u'''\n\nDTE CAF File Data Model\n\n''',
    'license': 'AGPL-3',
    'name': 'CAF Container for DTE Compliance',
    'test': [],
    'data': [
        'views/dte_caf.xml',
        'security/ir.model.access.csv',
    ],
    'update_xml': [],
    'version': '8.0.0.2',
    'website': 'http://blancomartin.cl',
    'installable': True,
    'auto_install': True,
    'active': False
}
