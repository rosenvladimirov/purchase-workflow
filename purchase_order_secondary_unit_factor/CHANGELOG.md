# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [18.0.1.0.0] - 2025-01-01

### Added
- Initial release for Odoo 18.0
- Secondary unit of measure support in purchase order lines
- **Editable conversion factor** for each purchase order line (key feature)
- Automatic calculation of primary quantity from secondary quantity
- Automatic calculation of secondary quantity from primary quantity
- Default factor loading from product secondary unit configuration
- Stock move integration with secondary unit information
- Demo data with example products and secondary units
- Comprehensive test coverage
- Bulgarian localization (bg.po translation file)
- User guide in Bulgarian (USER_GUIDE_BG.md)
- HTML description for Odoo Apps Store

### Features
- `secondary_uom_id` field on purchase.order.line
- `secondary_uom_qty` field on purchase.order.line
- `secondary_uom_factor` field on purchase.order.line (editable!)
- `secondary_uom_factor_editable` computed field
- Secondary unit fields on stock.move for traceability
- Onchange methods for automatic quantity calculations
- Tree and form view enhancements

### Technical
- Depends on: purchase, stock, product_secondary_unit
- Python version: 3.10+
- Odoo version: 18.0
- License: AGPL-3.0

### Documentation
- README.rst with full module documentation
- USER_GUIDE_BG.md with Bulgarian usage guide
- Comprehensive inline code documentation
- Demo data for testing

## Comparison with Standard OCA Module

### This Module (purchase_order_secondary_unit_factor)
- ✅ **Editable conversion factor per line**
- ✅ Can override product's default factor
- ✅ Flexible for special purchases
- ✅ No need to create new products for different packaging

### Standard OCA Module (purchase_order_secondary_unit)
- ❌ Fixed conversion factor from product
- ❌ Cannot override factor per line
- ❌ Less flexible for special cases

## Future Enhancements (Planned)

### Version 18.0.2.0.0
- [ ] Support for dynamic factor calculation based on supplier
- [ ] Price calculation per secondary unit
- [ ] Report templates showing secondary units
- [ ] Additional warehouse views with secondary units

### Version 18.0.3.0.0
- [ ] Integration with purchase agreements
- [ ] Supplier-specific default factors
- [ ] Historical factor tracking

## Migration Notes

### From purchase_order_secondary_unit to this module
If you are migrating from the standard OCA module `purchase_order_secondary_unit`:

1. The `secondary_uom_factor` field is new and will be populated with default values from products
2. Existing secondary quantities will be preserved
3. You can now edit factors - verify them after migration
4. Stock moves will start tracking the factor used

## Known Issues

None at this time.

## Contributors

- Rosen Vladimirov <rosen.vladimirov@digitalsprint.eu> - Initial development

## Maintainers

This module is maintained by the OCA.

[![Odoo Community Association](https://odoo-community.org/logo.png)](https://odoo-community.org)

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.
