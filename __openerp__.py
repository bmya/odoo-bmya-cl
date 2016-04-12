# -*- coding: utf-8 -*-
{
    'author': u'Blanco Martín & Asociados',
    'category': 'Localization/Chile',
    'depends': ['l10n_cl_invoice'],
    "external_dependencies": {
        'python': [
            'xmltodict',
            'base64'
        ]
    },
    'description': u'''\n\nIncorporate a field with the RUT (VAT) formatted 
according chilean customs.\n\n''',
    'installable': True,
    'license': 'AGPL-3',
    'name': 'CAF Container for DTE Compliance',
    'test': [],
    'data': [
        'views/dte_caf.xml',
        'security/ir.model.access.csv',
    ],
    'update_xml': [],
    'version': '0.0',
    'website': 'http://blancomartin.cl',
    'auto-install': False,
    'active': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
