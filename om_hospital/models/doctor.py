from odoo import api, fields, models , _


class HospitalDoctor(models.Model):
	_name = "hospital.doctor"
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_rec_name = 'name'


	name = fields.Char(string='Name', required=True, tracking=True)
	age = fields.Integer(string='Age',tracking=True)
	gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'female'),
        ('other', 'other'),
    ], required=True, default='male',tracking=True)	
	note = fields.Text(string='Description')
	image = fields.Binary(string="Patient Image") 
	appointment_count = fields.Integer(string="Appointment Count" , compute='_compute_appointment_count')
	active = fields.Boolean(string="Active", default=True)
	

	def copy(self, default=None):
		if default is None:
			default = {}
		if not default.get('name'):
			default['name'] = _("%s (Copy)", self.name)
		# default['note'] = "Coppied Record"
		return super(HospitalDoctor, self).copy(default)	

	def _compute_appointment_count(self):
		for rec in self:
			appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=' , rec.id)])
			rec.appointment_count = appointment_count			




       