# -*- coding: utf-8 -*-
{
    'name': 'Picking from XLS File',
    'author': u'Blanco Martín & Asociados',
    'category': 'Inventory',
    'depends': ['stock'],
    "external_dependencies": {
        'python': [
            'xlrd',
            'base64'
        ]
    },
    'license': 'LGPL-3',
    'price': 48.00,
    'currency': 'EUR',
    'test': [],
    'data': [
        'views/stock_picking_view.xml',
        ],
    'version': '11.0.1.0.0',
    'website': 'http://blancomartin.cl',
    'installable': False,
    'auto-install': False,
    'active': True
}
