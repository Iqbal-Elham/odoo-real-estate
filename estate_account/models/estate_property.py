# -*- coding: utf-8 -*-

from odoo import models, fields, api, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    invoice_id = fields.Many2one('account.move')
    invoice_amount = fields.Monetary(compute='_compute_invoice_amount' )
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    
    
    @api.depends('invoice_id')
    def _compute_invoice_amount(self):
        for record in self:
            record.invoice_amount = 0
            if record.invoice_id:
                record.invoice_amount = record.invoice_id.amount_total


    def sold_action(self):

        invoice = self.env['account.move'].create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'property_id': self.id,
            'currency_id': self.currency_id.id,

            'invoice_line_ids': [
                Command.create({
                    'name': '6% of the selling price',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': 'Administrative fee',
                    'quantity': 1,
                    'price_unit': 100,
                })
            ]
        })

        self.invoice_id = invoice.id

        return super(EstateProperty, self).sold_action()
    

    def open_invoice(self):
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'name': 'Invoice',
                'res_model': 'account.move',
                'res_id': rec.invoice_id.id,
            }
        
class MoveAccount(models.Model):
    _inherit = 'account.move'

    property_id = fields.Many2one('estate.property', string='Property')

    def open_property(self):
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'name': 'Property',
                'res_model': 'estate.property',
                'res_id': rec.property_id.id,
            }