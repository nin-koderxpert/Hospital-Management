from odoo import api, fields, models , _

class EstatePropertyType(models.Model):
	_name = "estate.property.type"
	_description = "Estate Property Type"
	_order = 'id DESC'
	_rec_name = "property_type"

	# name = fields.Char(string="Title")
	# property_type_id = fields.Many2one("res.partner", string="Partner")
	property_type = fields.Char(string="Property Type")
	property_ids = fields.One2many('estate.property', 'property_type_id', string="Property Id")
	# postcode = fields.Char(string="Pastcode")
	# available_from = fields.Date(string="Available From")
	property_count = fields.Integer(string="Property Count", compute="compute_property_count")
	offer_ids = fields.One2many('estate.property.offer','property_type_id',string="Offer Ids")
	offer_count = fields.Integer(string="Offer Count", compute='_compute_offer_count', store=True)
	_sql_constraints = [
			('unique_name', 'unique(name)', 'Property type name must be unique.')
		]

	def compute_property_count(self):
		for rec in self:
			rec.property_count = self.env['estate.property'].search_count([('property_type_id',"=",rec.id)])



	def _compute_offer_count(self):
		for rec in self:
			offer_count = self.env['estate.property.offer'].search_count([('property_type_id', '=' , rec.id)])
			rec.offer_count = offer_count		
	
	@api.depends('offer_ids')
	def _compute_offer_count(self):
		for record in self:
			record.offer_count = len(record.offer_ids)	

	# def action_view_offers(self):
	# 	action = self.env.ref('estate.action_estate_property_type').read()[0]
	# 	action['domain'] = [('property_type_id', '=', self.id)]
	# 	return action

	def action_view_properties(self):
		return {
            'type':'ir.actions.act_window',
            'name':'Offer',
            'res_model':'estate.property',
            'domain':[('property_type_id', '=' , self.id)],
            'context':{'default_property_type_id': self.id},
            'view_mode':'tree,form',
            'target':'current'
        } 


	def action_view_offers(self):
		properties = self.env['estate.property'].search([('property_type_id', '=', self.id)])
		return {
			'type': 'ir.actions.act_window',
			'name': 'Offers',
			'view_mode': 'tree,form',
			'res_model': 'estate.property.offer',
			'domain': [('partner_id', 'in', properties.ids)],
			'context': {'default_partner_id': self.env.context.get('default_partner_id')},
		}        




