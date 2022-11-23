{
    'name':"My University",
    'summary' : "your university from home",
    'description' : """
        Managing university etc
    """,
    'author' : "ilyes belbahi",
    'website': "www.donthaveawebsite.com",
    'category': "uncategorized",
    'version' : '13.0.1',
    'depends' : ['base','mail'],
    'images': ['static/src/img/default_image.png'],
    'data' : [
        'security/ir.model.access.csv',
        'views/university_student.xml','views/university_special.xml','views/university_prof.xml',
        'reports/student_report.xml',
        'reports/student_card_templates.xml',
    ],
    'demo' : ['demo.xml'],
}