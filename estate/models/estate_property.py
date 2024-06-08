from odoo import api, fields, models , _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class EstateProperty(models.Model):
	_name = "estate.property"
	__description = "Estate Property"
	_order = 'id DESC'


	name = fields.Char()
	agent_id = fields.Many2one('res.users', string='Agent')
	salesperson_id = fields.Many2one('res.users', string='Salesperson')
	note = fields.Text(string='Description')
	postcode = fields.Char(string="Pastcode")
	expected_price = fields.Float(string="Expected Price")
	bedrooms = fields.Integer(string="Bedrooms", default="2")
	available_from = fields.Date(string="Available From")
	selling_price = fields.Float(string="Selling Price",compute="_compute_selling_price")
    # state = fields.Selection([('draft','Draft'),('confirm','Confirm '),('done','Done'),('cancel',"Cancel"),],default='draft',string="Status",tracking=True)	
	states = fields.Selection([('new','New'), ('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')], default="new", string="State", tracking=True)
	facades = fields.Integer(string="Facades")
	garden = fields.Boolean(string="Garden")
	garden_orientation = fields.Selection([('north','North'),('south','South'),('east','East'),('west','West')], string="Garden Orientation")
	active = fields.Boolean(string="Active", default=True)
	property_type = fields.Char(string="Property TYpe")
	# sales_man = fields.Char(string="Sales Man")
	sales_man = fields.Many2one(comodel_name='res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
	buyer = fields.Many2one("res.partner", string="Buyer")
	property_type_id = fields.Many2one("estate.property.type", string="Property Type")
	tag_ids = fields.Many2many("estate.property.tag")
	offer_ids = fields.One2many("estate.property.offer", "property_id")	
	living_area = fields.Float(string="Living Area(sqm)")
	garden_area = fields.Float(string="Garden Area(sqm)")
	total_area = fields.Float(compute="_compute_total", string="Total Area(sqm)")
	best_price = fields.Float(compute="_compute_best_price", string="Best Price")
	count = fields.Many2one('estate.property.type', string="Count")
	state = fields.Selection([('cancel','Cancel'),('sold','Sold'),('new','New'),],default='new',string="Status",tracking=True, readonly=True)	
	# status = fields.Many2one("estate.property.offer", string="Satus")
	# salesperson_id = fields.Many2one(comodel_name='res.users', string='Salesperson')
	company_id = fields.Many2one(
        'res.company', 
        string='Company', 
        required=True, 
        default=lambda self: self.env.user.company_id
    )


	_sql_constraints = [
		('check_expected_price_positive', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.')
	]	


	@api.constrains('selling_price', 'expected_price')
	def _check_selling_price_(self):
		for product in self:
			# if product.selling_price and product.expected_price:
			if product.selling_price < 0.9 * product.expected_price:
				print('&&&&&&&&&&&&&&&', product.selling_price, 0.9 * product.expected_price)
				raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

	@api.constrains('selling_price')
	def check_selling_price(self):
		for rec in self:
			if rec.selling_price <=0 :
				raise ValidationError(_("Enter a positive price........."))				

	@api.depends('offer_ids.price')
	def _compute_best_price(self):
	    for record in self:
	        if record.offer_ids:
	            record.best_price = max(offer.price for offer in record.offer_ids)
	        else:
	            record.best_price = 0.0  # or any default value you prefer


	@api.depends('living_area','garden_area')
	def _compute_total(self):
		for record in self:
			record.total_area = record.living_area + record.garden_area

	


	def copy(self, default=None):
		if default is None:
			default = {}
		if not default.get('selling_price'):
			default['selling_price'] = _("%s (Copy)", self.selling_price)
		return super(EstateProperty, self).copy(default)

	def copy(self, default=None):
		if default is None:
			default = {}
		if not default.get('buyer'):
			default['buyer'] = _("%s (Copy)", self.buyer)
		
		return super(EstateProperty, self).copy(default)
		
	def copy(self, default=None):
		if default is None:
			default = {}
		if not default.get('available_from'):
			default['available_from'] = _("%s (Copy)", self.available_from)
		# default['note'] = "Coppied Record"
		return super(EstateProperty, self).copy(default)

	@api.onchange('garden')
	def onchange_garder_area(self):
		if self.garden:
			self.garden_area = 10
			self.garden_orientation = 'north'
		else:
			self.garden_area = 0
			self.garden_orientation = False	

	def action_cancel(self):
		for rec in self:
			if rec.states == 'sold':
				raise UserError("A sold property cannot be canceled.")
		rec.states = 'cancel'
		rec.offer_ids.status = 'refused'
        
	
	def action_sold(self):
		for rec in self:
			if rec.states == 'cancel':
				raise UserError("A canceled property cannot be set as sold.")
		rec.states = 'sold'	
		rec.offer_ids.status = 'accepted'

	
		
	@api.depends('offer_ids')
	def _compute_selling_price(self):
		for offer in self.offer_ids:
			if offer.status == 'accepted':
				self.buyer = offer.partner_id.id
				self.selling_price = offer.price
				break		

		else:
			self.selling_price = self.expected_price

	
	def unlink(self):
		for rec in self:
			if rec.states not in ['new','cancel']:
				raise UserError(_('You cannot delete a property unless its sate "New" or "Canceled"'))
		return super(rec, self).unlink()		

