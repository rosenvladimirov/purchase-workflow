# Copyright 2018 Tecnativa - Carlos Dauden
# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Purchase stock price unit sync',
    'summary': 'Update cost price in stock moves already done',
    'version': '11.0.2.0.0',
    'category': 'Purchase',
    'website': 'https://github.com/rosenvladimirov/purchase-workflow',
    'author': 'Rosen Vladimirov (BioPrint Ltd.), Tecnativa, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'installable': True,
    'depends': [
        'purchase',
        'account_recalculate_stock_move',
    ],
}
