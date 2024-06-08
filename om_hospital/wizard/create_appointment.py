from odoo import api, fields, models , _



class CreateAppointmentwizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment wizard"

    date_appointment = fields.Date(string='Date', required=True)
    patient_id=fields.Many2one('hospital.patient',string="Patient",required=True)
    doctor_id=fields.Many2one('hospital.doctor',string="Doctor",required=True)

    @api.model
    def default_get(self,fields):
        res = super(CreateAppointmentwizard, self).default_get(fields)
        if self._context.get('active_id'):
            res['patient_id'] = self._context.get('active_id')
        return res

    def action_create_appointment(self):
        vals = {
            'patient_id':self.patient_id.id,
            'doctor_id':self.doctor_id.id,
            'date_appointment':self.date_appointment
        }
        appointment_rec = self.env['hospital.appointment'].create(vals)
        return {
            'name':_('Appointment'),
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'res_model':'hospital.appointment',
            'res_id':appointment_rec.id,
            
                }

    def action_view_appointment(self):
        #method 1
        # action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]
        # action['domain'] = [('patient_id', '=' , self.patient_id.id)]

        #method 3
        # action = self.env['ir.actions.actions']._for_xml_id("om_hospital.action_hospital_appointment")
        # action['domain'] = [('patient_id', '=' , self.patient_id.id)]
        return {
            'type':'ir.actions.act_window',
            'name':'Appointment',
            'res_model':'hospital.appointment',
            'view_mode':'form',
            'domain':[('patient_id', '=' , self.patient_id.id)],
            'view_mode':'tree,form',
            'target':'current'           
        }
        # return action




