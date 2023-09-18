# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import ValidationError, UserError


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
    _order = "id desc"

    _sql_constraints = [
        (
            'positive_expected_price',
            'CHECK(expected_price >= 0)',
            'The expected price must be greater than 0'
        ),
        (
            'positive_selling_price',
            'CHECK(selling_price >= 0)',
            'The selling price must be greater than 0'
        )
    ]

    def unlink(self):
        for rec in self:
            if rec.state not in ('new', 'canceled'):
                raise UserError('You cannot delete a property that is not in the new or canceled state')
            return super(EstateProperty, self).unlink()

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for rec in self:
            if rec.selling_price < rec.expected_price * 0.9:
                raise ValidationError('The selling price must be greater than 90% of the expected price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offers_ids')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.offers_ids.mapped(lambda x: x.price)) if rec.offers_ids else 0
    
    @api.onchange('garden')
    def _onchange_garden(self):
        for rec in self:
            if rec.garden:
                rec.garden_area = 10
                rec.garden_orientation = 'north'
            else:
                rec.garden_area = 0
                rec.garden_orientation = ''
    

    def cancel_action(self):
        for rec in self:
            if rec.state == 'canceled':
                raise UserError('The state is already cancelled')
            elif rec.state == 'sold':
                raise UserError('The state is already sold')
            else:
                rec.state = 'canceled'
    
    def sold_action(self):
        for rec in self:
            if rec.state =='sold':
                raise UserError('The state is already sold')
            elif rec.state == 'canceled':
                raise UserError('The state is cancelled')
            else:
                rec.state ='sold'

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'This is the estate property type model'

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    _order = "name"
    sequence = fields.Integer()

    def open_offers(self):
        for rec in self:
            return {
                'name': 'Offers',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'estate.property.offer',
                'domain': [('property_type_id', '=', rec.id)],
            }
        
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'This is the estate property tag model'
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer()

    _sql_constraints = [
        (
            'unique_name',
            'UNIQUE(name)',
            'The name must be unique'
        )
    ]

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'This is the estate property offer model'
    # _rec_name = 'partner_id'
    _order = "price desc"

    property_id = fields.Many2one('estate.property', string="Property")
    partner_id = fields.Many2one('res.partner', string="Partner")
    price = fields.Float(string="Price", required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ])
    validity = fields.Integer()
    deadline_date = fields.Date(compute='_compute_deadline_date')

    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        (
            'positive_price',
            'CHECK(price >= 0)',
            'The price must be greater than 0'
        )
    ]

    @api.model
    def create(self, values):
        estate_property = self.env['estate.property'].browse(values.get('property_id'))
        estate_property.state = 'offer_received'
        if values.get('price') <= estate_property.best_price:
            raise ValidationError(f"The offer must be higher than {estate_property.best_price}")
        res = super(EstatePropertyOffer, self).create(values)
        return res


    @api.depends('create_date')
    def _compute_deadline_date(self):
        for rec in self:
            rec.deadline_date = rec.create_date + timedelta(days = rec.validity) if rec.create_date else False
    
    def accept_action(self):
        for rec in self:
            if rec.status == 'accepted':
                raise UserError('The status is already accepted')
            elif rec.status =='refused':
                raise UserError('The status is already refused')
            else:
                rec.status = 'accepted'
                rec.property_id.selling_price = rec.price
                rec.property_id.buyer = rec.partner_id
                rec.property_id.state = 'offer_accepted'
        
    def refuse_action(self):
        for rec in self:
            rec.status ='refused'