# -*- coding: utf-8 -*-

{
    'name' : 'Hospital Management',
    'version' : '1.0',
    'summary': 'Hospital Management Software',
    'sequence': -1,
    'description': """Hospital Management Software""",
    'category': 'Productivity',
    'website': 'https://www.odoomates.tech',
    'license':'LGPL-3',
    'depends' : ['sale',
                'mail',
                'report_xlsx',
                ],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/create_appointment_view.xml',
        'wizard/search_appointment_view.xml',
        'wizard/appointment_report_view.xml',
        'wizard/all_patient_report_view.xml',
        'views/patient.xml',
        'views/sale.xml',
        'views/appointment_view.xml',
        'views/doctor.xml',
        'views/kids_view.xml',
        'views/menu.xml',
        'views/patient_gender_view.xml',
        'report/report.xml',
        'report/patient_card.xml',
        'report/appointment_details.xml',
        'report/all_patient_list.xml',
        


    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
