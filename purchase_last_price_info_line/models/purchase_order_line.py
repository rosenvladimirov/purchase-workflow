# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    # related към компютнатите полета на продукта от purchase_last_price_info;
    # не се съхраняват — само за показване в реда на поръчката
    product_last_purchase_price = fields.Float(
        related="product_id.last_purchase_price",
        string="Last Purchase Price",
    )
    product_last_purchase_date = fields.Datetime(
        related="product_id.last_purchase_date",
        string="Last Purchase Date",
    )
    product_last_purchase_supplier_id = fields.Many2one(
        related="product_id.last_purchase_supplier_id",
        string="Last Supplier",
    )
