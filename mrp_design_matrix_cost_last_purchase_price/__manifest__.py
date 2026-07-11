# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "MRP Design Matrix Cost — Last Purchase Price",
    "version": "19.0.1.0.0",
    "category": "Manufacturing",
    "license": "AGPL-3",
    "author": "Rosen Vladimirov, Odoo Community Association (OCA)",
    "development_status": "Beta",
    "maintainers": ["rosenvladimirov"],
    "website": "https://github.com/rosenvladimirov/purchase-workflow",
    "summary": "Glue: feed the design-matrix cost engine the product's last "
    "purchase price from purchase_last_price_info, so verticals can cost on "
    "the last bought price instead of the product card standard cost",
    "depends": [
        "mrp_design_matrix_cost",
        "purchase_last_price_info",
    ],
    "installable": True,
    "auto_install": False,
}
