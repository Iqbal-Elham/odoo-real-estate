from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Transaction(models.Model):
    _name = 'banker.transaction'
    _description = 'Banker Transaction Model'

    name = fields.Many2one('res.partner', string='Customer', required=True)
    bank_id = fields.Many2one('banker.bank', string='Bank', required=True)

    balance = fields.Float('Balance')
    remarks = fields.Char('Remarks')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')])

    tran_state = fields.Selection([('deposit', 'Deposit'),
                                   ('withdraw', 'Withdraw')],
                                  string="Transaction Status", default='deposit', required=True)
    final_balance = fields.Float("Final Balance", compute="_get_final_balance")

    def _get_final_balance(self):
        for record in self:
            if record.state == "done":
                if record.tran_state == "withdraw":
                    record.final_balance = -(record.balance)
                else:
                    record.final_balance = record.balance
            else:
                record.final_balance =0.0
    
    def transaction_done(self):
        if self.tran_state == 'withdraw' and self.name.balance < self.balance:
            raise UserError(_("You don't have enough amount to withdraw."))
        self.state = 'done'
        # self.env.ref("wb_deposit_management.bank_transaction_done_email_template").send_mail(self.id, force_send=False)



