from odoo import api, fields, models , _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
	_name = "estate.property.offer"
	# _inherit = "res.partner"
	_description = "Offer"
	_order = 'id DESC'
	_rec_name = 'property_type_id'

	price = fields.Float(string="Price")
	status = fields.Selection([('accepted','Accepted'),('refused','Refused')], string="Status")

	partner_id = fields.Many2one('res.partner', string="Partner")
	property_id = fields.Many2one('estate.property', string="Property Id")
    # create_date = fields.Datetime(string="Create Date", readonly=True)
	create_date = fields.Datetime(string="Create Date", readonly=True)
	validity = fields.Integer(string='Validity(days)', default=30)
	date_deadline = fields.Datetime(string='Deadline', compute='_compute_date_deadline',inverse='_inverse_date_deadline', store=True)
	states = fields.Many2one('estate.property')
	property_type_id = fields.Many2one(related='property_id.property_type_id', string="Property Type", store=True)
	amount = fields.Float(string='Offer Amount', required=True)



	@api.model
	def create(self, vals):
		property_id = vals.get('property_id')
		new_offer_amount = vals.get('price')


		existing_offer = self.search([('property_id', '=', property_id)])


		for offer in existing_offer:
			if new_offer_amount <= offer.price:
				raise UserError(_('Cannot create an offer with an price lower than or equal to an existing offer.'))


		property = self.env['estate.property'].browse(property_id)
		property.states = 'offer_received'


		new_offer = super(EstatePropertyOffer, self).create(vals)
		return new_offer		

	@api.depends('status')
	def _compute_button_visibility(self):
		for record in self:
			record.is_accepted_visible = record.status == 'accepted'
			record.is_refused_visible = record.status == 'refused'



	is_accepted_visible = fields.Boolean(compute='_compute_button_visibility', store=True)
	is_refused_visible = fields.Boolean(compute='_compute_button_visibility', store=True)			

	# @api.depends('states')
	# def _compute_offer(self):
	# 	for rec in self:
	# 		if self.status == "accepted":
	# 			# self.states = "offer_received"

	@api.constrains('price')
	def check_price(self):
		for rec in self:
			if rec.price <=0:
				raise ValidationError(_("Enter a positive price........."))	

	
	@api.depends('create_date', 'validity')
	def _compute_date_deadline(self):
	    for rec in self:
	        if rec.create_date and rec.validity:
	            rec.date_deadline = rec.create_date + timedelta(days=rec.validity)
	        else:
	            rec.date_deadline = False  # Set to False or a default value if needed

	@api.depends('date_deadline')
	def _inverse_date_deadline(self):
		for record in self:
			if record.date_deadline:
				record.validity = (record.date_deadline - record.create_date).days if record.create_date else 0



	def action_accepted(self):
		self.accepted_clicked = True
		for rec in self:
			rec.status = 'accepted'
			rec.property_id.states = 'offer_accepted'


	def action_refused(self):
		self.refused_clicked = True
		for rec in self:
			rec.status = 'refused'
			rec.property_id.states = 'new'	


	accepted_clicked = fields.Boolean(string='Accepted Clicked')
	refused_clicked = fields.Boolean(string='Refused Clicked')


	@api.depends('accepted_clicked')
	def _compute_accepted_visible(self):
		for record in self:
			record.is_accepted_visible = not record.action_accepted


	@api.depends('refused_clicked')
	def _compute_refused_visible(self):
		for record in self:
			record.is_refused_visible = not record.action_refused                			


