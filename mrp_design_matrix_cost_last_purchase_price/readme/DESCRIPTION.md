This glue module bridges `purchase_last_price_info` and the design-matrix
cost engine (`mrp_design_matrix_cost`).

The cost engine costs BOM components on the product's ``standard_price`` (the
product card cost), falling back to an *inline* last-purchase-price lookup only
when ``standard_price`` is zero. This module:

* routes that fallback seam (``mrp.bom._last_po_price``) through the maintained
  ``purchase_last_price_info`` field, so "last purchase price" has a single
  source of truth; and
* exposes ``mrp.bom._design_last_purchase_cost(product)`` — a public helper a
  vertical industry module (e.g. Solid 55 doors) can call to cost on the last
  purchase price *as the primary source*, instead of materialising prices into
  ``standard_price``.

The engine's default behaviour (standard cost first) is left untouched — no
engine module is modified.
