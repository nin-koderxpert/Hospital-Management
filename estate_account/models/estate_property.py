from odoo import api, fields, models


class EstateInherit(models.Model):
	_inherit = 'estate.property'

	property_id = fields.Many2one('estate.property', string='Property', required=True)

	def action_sold(self):
		for record in self:
			property_id = record.property_id.id


			print(f"Attempting to create an invoice for property ID: {property_id}")

		res = super(EstateInherit, self).action_sold()

		self.create_invoice()

		print("action_sold method overridden in estate_account module.........")
		return res

		property_model = self.env['estate.property']
		try:
			property_model.check_access_rights('write')
		except AccessError:
			raise AccessError("You do not have the required permissions to update properties.")

            # Retrieve the property record
		property_record = property_model.browse(property_id)

            # Ensure the user has the required access rules
		try:
			property_record.check_access_rule('write')
		except AccessError:
			raise AccessError("You do not have the required permissions to update this property.")

	def create_invoice(self):
		commission = self.selling_price * 0.06

		admin_fee = 100.00

		invoice_vals = {
			'partner_id': self.buyer.id,
			'move_type': 'out_invoice',
			'invoice_date': fields.Date.today(),
			'invoice_line_ids': [
				(0,0, {
					'name': self.name,
					'quantity':1,
					'price_unit': commission,
					}),
				(0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1, 
                    'price_unit': admin_fee,
                }),
			],
		}
		invoice = self.env['account.move'].sudo().create(invoice_vals)
		return invoice