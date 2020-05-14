# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Reorganize views on Purchase order",
    "version": "11.0.1.0.0",
    "depends": ["purchase"],
    'author': "Rosen Vladimirov, "
              "Bioprint Ltd.",
    "website": 'https://github.com/rosenvladimirov/purchase-workflow',
    "category": "Purchases",
    "data": [
        "views/purchase_views.xml",
    ],
    'license': 'GPL-3',
    "auto_install": False,
    'installable': True,
}