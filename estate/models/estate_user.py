from odoo import models, fields, api

class EstateUser(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'salesman')