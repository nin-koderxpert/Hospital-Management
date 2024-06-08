from odoo import api, fields, models , _

class EstatePropertyTage(models.Model):
	_name = "estate.property.tag"
	_description = "Estate Property Tag"
	_order = 'id DESC'

	name = fields.Char()
	color = fields.Integer(string='Color')

	_sql_constraints = [
			('unique_name', 'unique(name)', 'Property Tag name must be unique.')
		]

