from odoo import api, fields, models

class AllPatientReport(models.AbstractModel):
	_name = 'report.om_hospital.report_all_patinet_list'
	_description = 'Patient Report' 


	@api.model
	def _get_report_values(self, docids, data=None):
		domain = []
		# gender = data.get('from_date').get('gender')
		# age = data.get('from_date').get('age')
		if data['form_data'].get('gender'):
			domain += [('gender', '=', data['form_data'].get('gender'))]
		if data['form_data'].get('age') and data['from_date'].get('age') != 0:
			domain += [('age', '=', data['form_data'].get('age'))]
			
		docs = self.env['hospital.patient'].search(domain)
		print('*************', domain, docs)

		return {
			'docs':docs,
			'email':'niramal@gamil.com',
		}


class PatientDetailsReport(models.AbstractModel):
	_name = "report.om_hospital.report_patient_details"
	_description = 'Patient Details Report'


	@api.model
	def _get_report_values(self, docids, data=None):
		docs = self.env['hospital.patient'].search([])
		return {
			'docs':docs,
		}	



