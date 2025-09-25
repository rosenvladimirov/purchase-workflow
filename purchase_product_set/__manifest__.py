# Copyright 2023 Rosen Vladimirov, BioPrint Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Purchase Product Set',
    'summary': """
        Add support for product set on purchase""",
    'version': '18.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Rosen Vladimirov, BioPrint Ltd.,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/purchase-workflow',
    'depends': [
        'purchase',
        'product_set'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_set_add.xml',
        'views/purchase_views.xml',
    ],
    'demo': [
    ],
}
