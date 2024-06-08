from odoo import models
import base64
import io

class PatientAppointmentXlsx(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_appointment_xls'
    _inherit = 'report.report_xlsx.abstract'



    def generate_xlsx_report(self, workbook, data, patients):
        print("mmmmmmmmmmmmmmmmm", data['appointments'])
        sheet = workbook.add_worksheet('Appointments')
        bold = workbook.add_format({'bold': True}) 
        sheet.set_column('D:D', 10)  
        sheet.set_column('E:E', 25)        

        row = 3
        col = 3

        sheet.write(row, col, 'Reference', bold)
        sheet.write(row, col + 1, 'Patient Name', bold)
        for appointment in data['appointments']:
            row += 1
            sheet.write(row, col, appointment['name'])
            sheet.write(row, col + 1, appointment['patient_id'][1])


        # sheet = workbook.add_worksheet("Patient ID Card")
        # bold = workbook.add_format({'bold':True})
        # format_1 = workbook.add_format({'bold':True, 'align': 'center', 'bg_color': 'yellow'})

        # row = 3
        # col = 3
        # sheet.set_column('D:D', 12) 

        # for obj in patients:
        #     row += 1
        #     sheet.merge_range(row, col, row, col + 1, 'ID Card', format_1)

        #     row += 1
        #     if obj.image:
        #         patient_image = io.BytesIO(base64.b64decode(obj.image))
        #         sheet.insert_image(row, col, "image.png", {'image_data':patient_image,'x_scale':0.5, 'y_scale':0.5})

        #         row += 5

        #     row += 1    
        #     # sheet.merge_range(row, col, row, col + 1,)
        #     sheet.write(row, col, 'Name', bold)#this is for labels
        #     sheet.write(row, col + 1, obj.name, bold)
        #     row += 1
        #     sheet.write(row, col, 'Age', bold)#this is for labels
        #     sheet.write(row, col + 1, obj.age, bold)
        #     row += 1
        #     sheet.write(row, col, 'Reference', bold)#this is for labels
        #     sheet.write(row, col + 1, obj.reference, bold)
        # for obj in patients:
        #     sheet = workbook.add_worksheet(obj.name)
        #     row = 3
        #     col = 3
        #     sheet.set_column('D:D', 12)  
        #     sheet.set_column('E:E', 13)

        #     row += 1
        #     sheet.merge_range(row, col, row, col + 1, 'ID Card', format_1)      

        #     row += 1
        #     if obj.image:
        #         patient_image = io.BytesIO(base64.b64decode(obj.image))
        #         sheet.insert_image(row, col, "image.png", {'image_data':patient_image,'x_scale':0.5, 'y_scale':0.5})

        #         row += 6

        #     row += 1    
        #     # sheet.merge_range(row, col, row, col + 1,)
        #     sheet.write(row, col, 'Name', bold)#this is for labels
        #     sheet.write(row, col + 1, obj.name, bold)
        #     row += 1
        #     sheet.write(row, col, 'Age', bold)#this is for labels
        #     sheet.write(row, col + 1, obj.age, bold)
        #     row += 1
        #     sheet.write(row, col, 'Reference', bold)#this is for labels
        #     sheet.write(row, col + 1, obj.reference, bold)  
            
        #     row += 2              



                   

