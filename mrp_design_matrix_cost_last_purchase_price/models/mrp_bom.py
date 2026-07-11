# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    # ── Лепило: канонична последна покупна цена (в costing мярката) ───────
    # mrp_design_matrix_cost има собствен inline `_last_po_price` (заявка към
    # purchase.order.line, БЕЗ зависимост към модул). Тук пренасочваме този
    # единствен seam към поддържания `purchase_last_price_info` — така
    # „последна покупна цена" има ЕДИН източник на истина (state purchase/done,
    # company scope).
    # ВАЖНО за коста: четем `price_unit_product_uom` на PO реда (core-ското поле
    # = `product_uom_id._compute_price(price_unit, product.uom_id)`), а НЕ суровия
    # price_unit — иначе покупка в различна мярка (напр. дузини) би внесла грешен
    # кост. Конверсията е на Odoo core, не наша.
    def _last_po_price(self, product):
        if not product:
            return 0.0
        line = getattr(product, "last_purchase_line_id", False)
        if line:
            price = line.price_unit_product_uom
            if price:
                return price
        return super()._last_po_price(product)

    # ── Публичен API за вертикалните индустрия модули (напр. Solid 55) ─────
    def _design_last_purchase_cost(self, product):
        """Върни цена за остойностяване с ПОСЛЕДНА ПОКУПНА цена като основен
        източник, fallback към standard_price (кост на продуктовия картон).

        Стандартната логика на енжина остава standard_price-first; вертикал,
        който иска да остойностява по реалната последна покупна цена (вместо
        да материализира цени в standard_price), вика този метод вместо да
        чете `product.standard_price` директно.

        Ред на резолюция:
          1. последна покупна цена (purchase_last_price_info)
          2. standard_price (продуктов картон)
          3. 0.0
        """
        if not product:
            return 0.0
        return (
            getattr(product, "last_purchase_price", 0.0)
            or product.standard_price
            or 0.0
        )
