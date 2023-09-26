# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Bank(models.Model):
    _name = 'banker.bank'
    _description = 'Banker Bank model'

    name = fields.Char(string='Bank Name', required=True)
    code = fields.Char(string='code', default='/', required=True)
    balance = fields.Float(string='balance', compute='_get_final_balance')
    partner_id = fields.Many2one('res.partner', string="Address")

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code("banker.bank")
        #Auto generate sequence for the bank profile.
        return super(Bank, self).create(vals)

    def _get_final_balance(self):
        tran_obj = self.env['banker.transaction']
        for record in self:
            all_transactions = tran_obj.search([('bank_id','=',record.id),('state','=','done')])
            all_deposit = sum(all_transactions.filtered(lambda lm:lm.tran_state == 'deposit').mapped("balance"))
            all_withdraw = sum(all_transactions.filtered(lambda lm:lm.tran_state == 'withdraw').mapped("balance"))
            record.balance = (all_deposit - all_withdraw) or 0.00

    _sql_constraints = [
        ('unique_banker_bank', 'unique(name)', 'Please provide unique bank name.'),
    ]