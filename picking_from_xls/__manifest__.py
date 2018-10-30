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
    'installable': False,
    'license': 'LGPL-3',
    'test': [],
    'data': [
        'views/stock_picking_view.xml',
        ],
    'version': '10.0',
    'website': 'http://blancomartin.cl',
    'auto-install': False,
    'active': True
}
