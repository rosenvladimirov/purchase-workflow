Install alongside a design-matrix vertical. With the module installed, the
engine's zero-cost fallback already resolves the canonical last purchase price.

To cost on the last purchase price as the **primary** source, have the vertical
call the helper instead of reading ``standard_price`` directly::

    unit_cost = bom._design_last_purchase_cost(product)

which resolves: last purchase price → ``standard_price`` → ``0.0``.
