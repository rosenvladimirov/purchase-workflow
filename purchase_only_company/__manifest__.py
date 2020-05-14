# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase order only by partner like company',
    'version': '11.0.1.0',
    'category': 'Purchases',
    'sequence': 61,
    'summary': 'When made Purchase Orders from contact partner, when confirm it to switch to partner',
    'description': "",
    'depends': ['purchase'],
    'data': [
        'views/purchase_views.xml',
    ],
    'test': [
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
}
