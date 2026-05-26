# Copyright 2025 Rosen Vladimirov
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import float_compare, float_is_zero


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    secondary_uom_factor = fields.Float(
        string="Conversion Factor",
        compute="_compute_secondary_uom_factor",
        inverse="_inverse_secondary_uom_factor",
        store=True,
        digits=(12, 6),
        default=1.0,
        help="Conversion factor between primary and secondary unit. "
        "This factor can be edited manually for each line.\n"
        "Example: If 1 Box = 12 Units, factor = 12.0\n"
        "Primary Qty = Secondary Qty * Factor",
    )
    secondary_uom_factor_editable = fields.Boolean(
        string="Factor Editable",
        readonly=True,
        help="Indicates if the conversion factor can be manually edited",
    )

    @api.depends("secondary_uom_qty", "secondary_uom_id")
    def _compute_secondary_uom_factor(self):
        for line in self:
            # Ако не е редактирано ръчно, взимаме стандартния фактор
            if not line.secondary_uom_factor_editable:
                line.secondary_uom_factor = line._get_factor_line()
            # Важно: Ако е редактирано (editable=True), Odoo ще запази текущата стойност в базата,
            # така че не е нужно да правим нищо в else, освен ако полето няма стойност.
            elif not line.secondary_uom_factor:
                 line.secondary_uom_factor = line._get_factor_line()

    def _inverse_secondary_uom_factor(self):
        for line in self:
            theoretical_factor = line._get_factor_line()
            # Използваме float_compare за безопасно сравнение
            # precision_digits=6 съвпада с дефиницията на полето digits=(12, 6)
            if float_compare(line.secondary_uom_factor, theoretical_factor, precision_digits=6) != 0:
                line.secondary_uom_factor_editable = True
                self._compute_helper_target_field_qty()
            else:
                line.secondary_uom_factor_editable = False
                # Възстановяваме точния теоретичен фактор, за да избегнем микро-разлики
                line.secondary_uom_factor = theoretical_factor

    def _get_factor_line(self):
        if self.secondary_uom_factor_editable:
            return self.secondary_uom_factor
        return super()._get_factor_line()
