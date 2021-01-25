# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import AccessError

import logging
_logger = logging.getLogger(__name__)


class PurchaseOrderLinePriceHistory(models.TransientModel):
    _name = "purchase.order.line.price.history"
    _description = "Purchase order line price history"

    @api.model
    def _default_partner_id(self):
        line_id = self.env.context.get("active_id")
        return self.env['purchase.order.line'].browse(line_id).partner_id.id

    purchase_order_line_id = fields.Many2one(
        comodel_name='purchase.order.line',
        string='purchase order line',
        default=lambda self: self.env.context.get("active_id"),
    )
    product_id = fields.Many2one(
        related="purchase_order_line_id.product_id",
        readonly=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        default=_default_partner_id,
    )
    line_ids = fields.One2many(
        comodel_name="purchase.order.line.price.history.line",
        inverse_name="purchase_history_id",
        string="History line",
        readonly=True,
    )
    move_line_ids = fields.One2many(
        comodel_name="stock.move.line.price.history.line",
        inverse_name="purchase_history_id",
        string="History moves",
        readonly=True,
    )
    include_quotations = fields.Boolean(
        string="Include quotations",
        help="Include quotations lines in the purchase history",
    )
    include_commercial_partner = fields.Boolean(
        string="Include commercial entity",
        default=True,
        help="Include commercial entity and its contacts in the purchase history"
    )
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Pricelist',
        compute_sudo=True,
        help="Pricelist for current purchases order."
    )

    @api.onchange("partner_id", "include_quotations",
                  "include_commercial_partner")
    def _onchange_partner_id(self):
        self.line_ids = False
        self.move_line_ids = False
        move_ids = self.env['stock.move']
        states = ["purchase", "done"]
        move_states = ["done"]
        if self.include_quotations:
            states += ["draft", "sent"]
        domain = [
            ("product_id", "=", self.product_id.id),
            ("state", "in", states),
        ]
        if self.partner_id and not self._context.get('force_remove_partner'):
            if self.include_commercial_partner:
                domain += [("partner_id", "child_of",
                            self.partner_id.commercial_partner_id.ids)]
            else:
                domain += [
                    ("partner_id", "child_of", self.partner_id.ids)]

        vals = []
        order_lines = self.env['purchase.order.line'].search(domain, limit=20)
        order_lines -= self.purchase_order_line_id
        for order_line in order_lines:
            move_ids |= order_line.move_ids
            vals.append((0, False, {
                'purchase_order_line_id': order_line.id,
                'history_purchase_order_line_id': self.purchase_order_line_id,
            }))
        self.line_ids = vals
        vals = []
        for move_line in move_ids:
            if move_line.state in move_states:
                for line in move_line.move_line_ids:
                    vals.append((0, False, {
                        'stock_move_line_id': line.id,
                        'history_purchase_order_line_id': self.purchase_order_line_id,
                    }))
        self.move_line_ids = vals


class PurchaseOrderLinePriceHistoryline(models.TransientModel):
    _name = "purchase.order.line.price.history.line"
    _description = "Purchase order line price history line"

    purchase_history_id = fields.Many2one(
        comodel_name="purchase.order.line.price.history",
        string="History",
    )
    history_purchase_order_line_id = fields.Many2one(
        comodel_name='purchase.order.line',
        string="history purchase order line",
    )
    purchase_order_line_id = fields.Many2one(
        comodel_name='purchase.order.line',
        string='purchase order line',
    )
    order_id = fields.Many2one(
        related="purchase_order_line_id.order_id",
        readonly=True,
    )
    currency_id = fields.Many2one(
        related="purchase_order_line_id.currency_id",
        readonly=True,
    )
    partner_id = fields.Many2one(
        related="purchase_order_line_id.partner_id",
        readonly=True,
    )
    purchase_order_date_order = fields.Datetime(
        related="purchase_order_line_id.order_id.date_order",
        readonly=True,
    )
    purchase_order_product_id = fields.Many2one(
        related="purchase_order_line_id.product_id",
        readonly=True,
    )
    product_qty = fields.Float(
        related="purchase_order_line_id.product_qty",
        readonly=True,
    )
    price_unit = fields.Float(
        related="purchase_order_line_id.price_unit",
        readonly=True,
    )
    product_uom = fields.Many2one(
        related='purchase_order_line_id.product_uom',
        readonly=True,
    )

    @api.multi
    def action_set_price(self):
        self.ensure_one()
        self.history_purchase_order_line_id.price_unit = self.price_unit

    @api.model
    def get_value_pricelist(self, lwrite=False):
        if lwrite:
            res = {'name': self.partner_id.id,
                   'price': self.price_unit}
        else:
            res = {'price': self.price_unit}
        if self.purchase_order_product_id.product_tmpl_id.product_variant_count > 0:
            res.update({'product_id':  self.purchase_order_product_id.id})
        else:
            res.update({'product_tmpl_id': self.purchase_order_product_id.product_tmpl_id.id})
        return res

    @api.multi
    def save_in_pricelist(self):
        self.ensure_one()
        #_logger.info("PRICELIST %s" % self.history_purchase_order_line_id.order_id.pricelist_id)
        order = self.history_purchase_order_line_id.order_id
        line = self.history_purchase_order_line_id
        partner = order.partner_id if not order.partner_id.parent_id else order.partner_id.parent_id
        product_id = self.purchase_order_product_id
        supplierinfo = self.env['product.supplierinfo'].search([('name', '=', partner.id), "|",
                                                                ('product_id', '=', product_id.id),
                                                                ('product_tmpl_id', '=', product_id.product_tmpl_id.id)])
        # _logger.info("SAVE PRICELIST %s" % self.get_value_pricelist())
        if supplierinfo:
            supplierinfo.write(self.get_value_pricelist(False))
        elif partner not in line.product_id.seller_ids.mapped('name') and len(line.product_id.seller_ids) <= 10:
            supplierinfo = self.get_value_pricelist(False)
            supplierinfo.update({{
                'sequence': max(line.product_id.seller_ids.mapped('sequence')) + 1 if line.product_id.seller_ids else 1,
                'min_qty': 0.0,
                'currency_id': self.currency_id.id,
                'delay': 0,
            }})
            # In case the order partner is a contact address, a new supplierinfo is created on
            # the parent company. In this case, we keep the product name and code.
            seller = line.product_id._select_seller(
                partner_id=line.partner_id,
                quantity=line.product_qty,
                date=line.order_id.date_order and line.order_id.date_order[:10],
                uom_id=line.product_uom)
            if seller:
                supplierinfo['product_name'] = seller.product_name
                supplierinfo['product_code'] = seller.product_code
            vals = {
                'seller_ids': [(0, 0, supplierinfo)],
            }
            try:
                line.product_id.write(vals)
            except AccessError:  # no write access rights -> just ignore
                pass


class StockMoveLinePriceHistoryline(models.TransientModel):
    _name = "stock.move.line.price.history.line"
    _description = "Stock move line price history line"

    purchase_history_id = fields.Many2one(
        comodel_name="purchase.order.line.price.history",
        string="History",
    )
    history_purchase_order_line_id = fields.Many2one(
        comodel_name='purchase.order.line',
        string="history purchase order line",
    )
    stock_move_line_id = fields.Many2one(
        comodel_name='stock.move.line',
        string='purchase order line',
    )
    move_id = fields.Many2one(
        related="stock_move_line_id.move_id",
        readonly=True,
    )
    picking_id = fields.Many2one(
        related="stock_move_line_id.picking_id",
        readonly=True,
    )
    partner_id = fields.Many2one(
        related="stock_move_line_id.picking_id.partner_id",
        readonly=True,
    )
    stock_move_order_date_order = fields.Datetime(
        related="stock_move_line_id.picking_id.date_done",
        readonly=True,
    )
    purchase_order_product_id = fields.Many2one(
        related="stock_move_line_id.product_id",
        readonly=True,
    )
    lot_id = fields.Many2one(
        related="stock_move_line_id.lot_id",
        readonly=True,
    )
    purchase_line_id = fields.Many2one(
        related="stock_move_line_id.move_id.purchase_line_id",
        readonly=True,
    )
    purchase_id = fields.Many2one(
        related="stock_move_line_id.move_id.purchase_line_id.order_id",
        readonly=True,
    )
    qty_done = fields.Float(
        related="stock_move_line_id.qty_done",
        readonly=True,
    )
    #purchase_price_unit = fields.Many2one(
    #    related="stock_move_line_id.move_id.purchase_line_id.price_unit",
    #    readonly=True,
    #)
    purchase_currency_id = fields.Many2one(
        related="stock_move_line_id.move_id.purchase_line_id.order_id.currency_id",
        readonly=True,
    )
    price_unit = fields.Float(
        related="stock_move_line_id.move_id.price_unit",
        readonly=True,
    )
    product_uom = fields.Many2one(
        related='stock_move_line_id.move_id.product_uom',
        readonly=True,
    )

    @api.multi
    def action_set_price(self):
        self.ensure_one()
        self.history_purchase_order_line_id.price_unit = self.price_unit
