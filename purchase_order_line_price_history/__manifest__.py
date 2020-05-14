# Copyright 2019 Tecnativa - Ernesto Tejeda
# Copyright 2019 dXFactory - Rosen Vladimirov
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase order line price history",
    "version": "11.0.1.0.0",
    "category": "Purchases",
    "author": "Rosen Vladimirov, "
              "dXFactory Ltd, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/rosenvladimirov/purchase-workflow/",
    "license": "AGPL-3",
    "depends": [
        "sale",
    ],
    "data": [
        "wizards/purchase_orderLine_price_history.xml",
        "views/purchase_views.xml",
    ],
    "installable": True,
}
