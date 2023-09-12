# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, timedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'This is the estate property model'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Post code")
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living area")
    date_availability = fields.Date(string="Date", copy=False, default=lambda self: date.today() + timedelta(90))
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(string="Active", default=False)
    state = fields.Selection([
        ('new', 'New'), 
        ('offer_received', 'Offer Received'), 
        ('offer_accepted', 'Offer Accepted'), 
        ('sold', 'Sold'), 
        ('canceled', 'Canceled')
        ], default='new', required=True, copy=False)

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    property_tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    salesman = fields.Many2one('res.users', default= lambda self: self.env.uid)
    buyer = fields.Many2one('res.partner', default='')

    offers_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')

    total_area = fields.Float(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offers_ids')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.offers_ids.mapped(lambda x: x.price)) if rec.offers_ids else 0

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'This is the estate property type model'

    name = fields.Char(string="Name", required=True)

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'This is the estate property tag model'

    name = fields.Char(string="Name", required=True)

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'This is the estate property offer model'

    property_id = fields.Many2one('estate.property', string="Property")
    partner_id = fields.Many2one('res.partner', string="Partner")
    price = fields.Float(string="Price", required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ])
    validity = fields.Integer()