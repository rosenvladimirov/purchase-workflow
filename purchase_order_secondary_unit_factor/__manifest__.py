# Copyright 2025 Rosen Vladimirov
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Order Secondary Unit with Editable Factor",
    "summary": "Add editable conversion factor for secondary units in purchase orders",
    "version": "18.0.1.0.0",
    "category": "Purchases",
    "website": "https://github.com/OCA/purchase-workflow",
    "author": "Rosen Vladimirov, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase",
        "purchase_stock",
        "stock",
        "product_secondary_unit",
        "purchase_order_secondary_unit"
    ],
    "data": [
        "views/purchase_order_views.xml",
    ],
    "demo": [
        "demo/product_demo.xml",
    ],
}
