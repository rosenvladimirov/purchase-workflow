#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.tools import groupby

_logger = logging.getLogger(__name__)


class PurchaseOrderLine(models.Model):
    _name = 'purchase.order.line'
    _inherit = ['purchase.order.line', 'product.set.mixin']

    product_set_section_id = fields.Many2one('purchase.order.line', string='Sale Product Set Section')

    def _prepare_account_move_line(self, move=False):
        values = super()._prepare_account_move_line(move=move)
        self.ensure_one()
        values.update({
            'product_set_id': self.product_set_id.id,
            'product_set_line_id': self.product_set_line_id.id
        })
        return values

    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        values = super()._prepare_stock_move_vals(picking, price_unit, product_uom_qty, product_uom)
        values.update({
            'product_set_id': self.product_set_id.id,
            'product_set_line_id': self.product_set_line_id.id
        })
        return values

    def _get_values_product_set_mixin(self, total_quantity):
        res = self._get_update_product_set_section_values(total_quantity)
        res.update({
            'product_qty': 0,
            'price_unit': 0,
        })
        return res

    @api.model_create_multi
    def create(self, vals_list):
        if not self._context.get('create_new_set'):
            self._add_product_set_sections('purchase.order', vals_list)
        return super().create(vals_list)

    def write(self, values):
        if not self._context.get('create_new_set') and values.get('product_set_id'):
            self._set_product_set_sections('purchase.order', values)
        return super().write(values)

    def unlink(self):
        self._unlink_product_set_sections()
        return super().unlink()
