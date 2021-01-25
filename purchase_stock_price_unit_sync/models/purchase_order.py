# Copyright 2019 Carlos Dauden - Tecnativa <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def _get_stock_move_price_unit(self):
        if not self._context.get('force_account_date'):
            return super(PurchaseOrderLine, self)._get_stock_move_price_unit()
        else:
            self.ensure_one()
            line = self[0]
            order = line.order_id
            price_unit = line.price_unit
            if line.taxes_id:
                price_unit = line.taxes_id.with_context(round=False).compute_all(
                    price_unit, currency=line.order_id.currency_id, quantity=1.0, product=line.product_id, partner=line.order_id.partner_id
                )['total_excluded']
            if line.product_uom.id != line.product_id.uom_id.id:
                price_unit *= line.product_uom.factor / line.product_id.uom_id.factor
            if order.currency_id != order.company_id.currency_id:
                price_unit = order.currency_id.with_context(date=self._context['force_account_date']).compute(price_unit, order.company_id.currency_id, round=False)
        return price_unit


    def write(self, vals):
        res = super().write(vals)
        if ('price_unit' in vals or 'discount' in vals) and (
                not self.env.context.get('skip_stock_price_unit_sync')):
            self.stock_price_unit_sync()
        return res

    def stock_price_unit_sync(self):
        for line in self.filtered(lambda l: l.state in ['purchase', 'done']):
            for move in line.move_ids:
                date = move.accounting_date or move.date
                move.write({
                    'price_unit': line.with_context(skip_stock_price_unit_sync=True, force_account_date=date)._get_stock_move_price_unit(),
                })
