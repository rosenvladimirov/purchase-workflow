# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    partner_contact_id = fields.Many2one('res.partner', string='Vendor Contact', required=True, states={
                            'purchase': [('readonly', True)],
                            'done': [('readonly', True)],
                            'cancel': [('readonly', True)],
                            }, change_default=True, track_visibility='always')

    @api.onchange('partner_contact_id')
    def onchange_partner_contact_id(self):
        if self.partner_contact_id:
            self.partner_id = self.partner_contact_id.parent_id
            return {'domain': {'partner_id': [('id', '=', self.partner_contact_id.parent_id.id), ('supplier','=', True), ('is_company', '=', True)]}}
        return {'domain': {'partner_id': [('supplier','=', True), ('is_company', '=', True)]}}

    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        res = super(PurchaseOrder, self).onchange_partner_id()
        if (not self.partner_contact_id and self.partner_id) or (self.partner_contact_id and self.partner_id and self.partner_contact_id.parent_id != self.partner_id):
            self.partner_contact_id = self.partner_id.child_ids and self.partner_id.mapped('child_ids')[0] or False
            if self.partner_contact_id:
                if not res:
                    res = {}
                res.update({'domain': {'partner_contact_id': [('parent_id', '=', self.partner_id.id), ('supplier','=', True), ('is_company', '=', False)]}})
        return res

    @api.model
    def create(self, vals):
        if 'partner_id' in vals and not vals.get('partner_contact_id', False):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            vals['partner_contact_id'] = partner.child_ids and partner.mapped('child_ids')[0].id or vals.get('partner_id')
        return super(PurchaseOrder, self).create(vals)
