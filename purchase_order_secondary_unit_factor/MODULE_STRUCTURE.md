# Purchase Order Secondary Unit Factor - Module Structure

## Overview

This is a complete Odoo 18.0 module that extends purchase orders with editable secondary units and conversion factors.

## Key Innovation

**Editable Conversion Factor**: Unlike the standard OCA module where the factor is fixed, this module allows editing the conversion factor directly in each purchase order line.

## Directory Structure

```
purchase_order_secondary_unit_factor/
├── __init__.py                          # Module initialization
├── __manifest__.py                      # Module manifest and metadata
├── README.rst                           # Full documentation (English)
├── USER_GUIDE_BG.md                    # User guide in Bulgarian
├── CHANGELOG.md                         # Version history
│
├── models/                              # Business logic
│   ├── __init__.py
│   ├── purchase_order_line.py          # Main model with editable factor
│   └── stock_move.py                   # Stock integration
│
├── views/                               # User interface
│   └── purchase_order_views.xml        # Form and tree views
│
├── demo/                                # Demo/sample data
│   └── product_demo.xml                # Example products with secondary units
│
├── tests/                               # Automated tests
│   ├── __init__.py
│   └── test_purchase_order_secondary_unit_factor.py  # Unit tests
│
├── i18n/                                # Translations
│   └── bg.po                           # Bulgarian translation
│
└── static/                              # Static assets
    └── description/
        └── index.html                  # App store description page
```

## File Descriptions

### Core Files

#### `__manifest__.py`
- Module metadata, dependencies, and data files
- Version: 18.0.1.0.0
- License: AGPL-3
- Dependencies: purchase, stock, product_secondary_unit

#### `models/purchase_order_line.py`
**Key features:**
- `secondary_uom_id`: Link to secondary unit
- `secondary_uom_qty`: Quantity in secondary unit
- `secondary_uom_factor`: **EDITABLE** conversion factor (main innovation!)
- `secondary_uom_factor_editable`: Indicates if factor can be edited
- Automatic quantity calculations (bidirectional)
- Onchange methods for user experience
- Stock move preparation with secondary unit data

**Important methods:**
- `_onchange_product_id_secondary_unit()`: Loads default from product
- `_onchange_secondary_uom_id()`: Updates factor when unit changes
- `_onchange_secondary_uom_qty()`: Calculates primary qty
- `_onchange_product_qty_secondary_unit()`: Calculates secondary qty
- `_prepare_stock_move_vals()`: Passes data to stock moves

#### `models/stock_move.py`
- Extends stock.move with secondary unit fields
- Ensures traceability through warehouse operations

### View Files

#### `views/purchase_order_views.xml`
Three view enhancements:
1. **Form view**: Full form with editable fields
2. **Tree view in PO**: Shows secondary unit columns
3. **Standalone tree view**: For line lists

### Demo Data

#### `demo/product_demo.xml`
- Example product: Screws (Units with Box and Pallet)
- Example product: Cables (Meters with Roll)
- Ready-to-use secondary units

### Tests

#### `tests/test_purchase_order_secondary_unit_factor.py`
**Test coverage:**
1. `test_01_secondary_qty_calculation`: Secondary → Primary calculation
2. `test_02_primary_qty_calculation`: Primary → Secondary calculation
3. `test_03_editable_factor`: Factor editing functionality
4. `test_04_factor_change_with_secondary_qty`: Dynamic recalculation
5. `test_05_default_factor_from_product`: Auto-loading defaults
6. `test_06_no_secondary_unit`: Behavior without secondary unit
7. `test_07_stock_move_vals`: Stock integration

### Documentation

#### `README.rst`
- Full English documentation
- Installation instructions
- Usage examples
- Bug tracker information
- OCA standard format

#### `USER_GUIDE_BG.md`
- Complete Bulgarian user guide
- Configuration steps
- Use case scenarios
- FAQ section
- Example configurations for different industries

#### `CHANGELOG.md`
- Version history
- Feature list
- Comparison with standard module
- Future enhancements
- Migration notes

### Translations

#### `i18n/bg.po`
Complete Bulgarian translation for:
- Field labels
- Help texts
- View elements
- All user-facing strings

## Key Features Implementation

### 1. Editable Factor
```python
secondary_uom_factor = fields.Float(
    string="Conversion Factor",
    digits=(12, 6),
    default=1.0,
    help="This factor can be edited manually for each line."
)
```

### 2. Automatic Calculations
Formula: `Primary Qty = Secondary Qty × Factor`

Implemented through:
- `@api.onchange('secondary_uom_qty', 'secondary_uom_factor')`
- `@api.onchange('product_qty')`

### 3. Stock Integration
```python
def _prepare_stock_move_vals(self, picking):
    vals = super()._prepare_stock_move_vals(picking)
    if self.secondary_uom_id:
        vals.update({
            'secondary_uom_id': self.secondary_uom_id.id,
            'secondary_uom_qty': self.secondary_uom_qty,
            'secondary_uom_factor': self.secondary_uom_factor,
        })
    return vals
```

## Usage Flow

1. **User creates PO** → Selects product
2. **System loads** → Default secondary unit and factor from product
3. **User can** → Edit factor if needed (special packaging)
4. **User enters** → Quantity in either primary or secondary
5. **System calculates** → Other quantity automatically
6. **On confirm** → Data flows to stock moves

## Differences from Standard OCA Module

| Feature | This Module | Standard Module |
|---------|------------|-----------------|
| Factor source | Product + **Editable per line** | Product only (fixed) |
| Special packaging | ✅ Just edit factor | ❌ Must create new product |
| Flexibility | High | Limited |
| Use case | Variable packaging | Standard packaging only |

## Installation Requirements

### Dependencies
1. **purchase** (Odoo core)
2. **stock** (Odoo core)
3. **product_secondary_unit** (OCA module)

### Installation Steps
```bash
# 1. Install dependencies
# Ensure product_secondary_unit is installed

# 2. Copy module to addons path
cp -r purchase_order_secondary_unit_factor /path/to/odoo/addons/

# 3. Update apps list
# Odoo: Apps → Update Apps List

# 4. Install module
# Odoo: Apps → Search "Purchase Order Secondary Unit Factor" → Install
```

## Testing

Run tests:
```bash
odoo-bin -c odoo.conf -d database_name -u purchase_order_secondary_unit_factor --test-enable --stop-after-init
```

## Contributing

This module follows OCA guidelines:
- PEP8 compliant
- Full test coverage
- Proper documentation
- i18n support

## License

AGPL-3.0 - See LICENSE file

## Author

**Rosen Vladimirov**
- Email: rosen.vladimirov@digitalsprint.eu
- Specialized in Bulgarian Odoo localization
- OCA contributor

## Maintainer

**Odoo Community Association (OCA)**
- Website: https://odoo-community.org
- GitHub: https://github.com/OCA/purchase-workflow

## Support

- Issues: https://github.com/OCA/purchase-workflow/issues
- Discussions: https://github.com/OCA/purchase-workflow/discussions
