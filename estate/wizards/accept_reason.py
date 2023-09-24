# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class AcceptReasonWizard(models.TransientModel):
    _name = 'accept.reason.wizard'
    _description = 'Accept reasons wizard'

    reason = fields.Text(required=True)
    date = fields.Date(default=fields.Date.context_today)
    property_id = fields.Many2one('estate.property')
    offer_id = fields.Many2one('estate.property.offer')

    def accept_action(self):
        for rec in self:
            if rec.offer_id.status == 'accepted':
                raise UserError('The status is already accepted')
            elif rec.offer_id.status =='refused':
                raise UserError('The status is already refused')
            else:
                rec.property_id.write({
                    'selling_price': rec.offer_id.price,
                    'buyer': rec.offer_id.partner_id.id,
                    'state': 'offer_accepted',
                    'offer_accept_reason': rec.reason,
                })
                rec.offer_id.status = 'accepted'