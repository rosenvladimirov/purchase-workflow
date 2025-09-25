#  Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class PurchaseProductSet(models.Model):
    _name = 'purchase.product.set'
    _description = 'Sale Product Sets'

    order_id = fields.Many2one('purchase.order', 'Purchase Order', required=True)
    product_set_id = fields.Many2one('product.set', 'Product Set')
    quantity = fields.Float('Quantity', digits='Product Unit of Measure')
    price_unit = fields.Float('Unit Price', compute='_compute_price_unit', store=True, precompute=True)
    price_subtotal = fields.Monetary(string="Subtotal")
    currency_id = fields.Many2one('res.currency', related='order_id.currency_id')

    @api.depends('quantity', 'price_subtotal')
    def _compute_price_unit(self):
        for line in self:
            quantity = line.quantity != 0.0 and line.quantity or 1.0
            line.update({
                'price_unit': line.price_subtotal / quantity,
            })

    @staticmethod
    def _get_purchase_product_set_value(order_id, product_set_id, price_subtotal, quantity):
        return {
            'order_id': order_id.id,
            'product_set_id': product_set_id.id,
            'price_subtotal': price_subtotal,
            'quantity': quantity,
        }
