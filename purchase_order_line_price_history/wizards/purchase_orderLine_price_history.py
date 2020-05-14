# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _

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
        inverse_name="history_id",
        string="History line",
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
        states = ["purchase", "done"]
        if self.include_quotations:
            states += ["draft", "sent"]
        domain = [
            ("product_id", "=", self.product_id.id),
            ("state", "in", states),
        ]
        if self.partner_id:
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
            vals.append((0, False, {
                'purchase_order_line_id': order_line.id,
                'history_purchase_order_line_id': self.purchase_order_line_id,
            }))
        self.line_ids = vals


class PurchaseOrderLinePriceHistoryline(models.TransientModel):
    _name = "purchase.order.line.price.history.line"
    _description = "Purchase order line price history line"

    history_id = fields.Many2one(
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
        if self.purchase_order_product_id > 0:
            res.update({'product_id':  self.purchase_order_product_id.id})
        else:
            res.update({'product_tmpl_id': self.purchase_order_product_id.product_tmpl_id.id})
        return res

    @api.multi
    def save_in_pricelist(self):
        self.ensure_one()
        #_logger.info("PRICELIST %s" % self.history_purchase_order_line_id.order_id.pricelist_id)
        if self.history_purchase_order_line_id.order_id.pricelist_id:
            pricelist_id = self.history_purchase_order_line_id.order_id.pricelist_id
            product_id = self.purchase_order_product_id
            supplierinfo = self.env['product.supplierinfo'].search([('name', '=', self.partner_id.id), "|",
                                                                           ('product_id', '=', product_id.id),
                                                                           ('product_tmpl_id', '=', product_id.product_tmpl_id.id)])
            _logger.info("SAVE PRICELIST %s" % self.get_value_pricelist())
            if supplierinfo:
                supplierinfo.write(self.get_value_pricelist(False))
            else:
                self.env['product.supplierinfo'].create(self.get_value_pricelist(True))
