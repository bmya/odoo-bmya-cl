{
    'name': 'Relate purchase order with invoice',
    'version': '1.0.1',
    'category': 'Purchase',
    'description': """
This module establish a relationship between purchase order and the invoice, from an already generated invoice
perspective.
It checks if the invoice matches the purchase order but without adding the purchase order lines to the invoice.
This module changes the original behaviour of Odoo, since it prevents to replicate the lines in the invoice and
Allows the operator to have several criterias for approving or rejecting the invoice if it is generated from an
external source, or if it is generated from account module without following the natural purchase workflow in Odoo. 
    """,
    'author': 'Blanco Martin & Asociados',
    'website': 'http://blancomartin.cl',
    'license': 'LGPL-3',
    'depends': [
        'purchase',
        ],
    'data': [
        'views/account_move_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}