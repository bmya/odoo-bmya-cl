# -*- coding: utf-8 -*-
{
    'name': 'BMYA Modules Configuration',
    'version': '1.0',
    'category': 'BMYA Modules',
    'summary': 'extra, addons, modules',
    'description': """
BMYA Modules Configuration
==========================
Here, you can configure various business features. \nYou'll be provided 
different configuration options in the Settings where by only selecting 
some booleans you will be able to install several modules and apply access 
rights in just one go.
    """,
    'author':  'Blanco Martin & Asociados',
    'website': 'http://blancomartin.cl',
    'images': [
    ],
    'depends': [
        'base_setup',
        'website',
        'mail'
    ],
    'data': [
        'views/res_config_view.xml',
        # 'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'views/res_groups_view.xml',
    ],
    'demo': [
        'demo/company_demo.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': True,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
