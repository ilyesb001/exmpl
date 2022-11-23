import base64
from logging import warning
from odoo.modules.module import get_module_resource
from odoo import models,fields,api,exceptions,modules         
from datetime import datetime,timedelta

# class resStud (models.Model):
#     _inherit='res.users'
#     student_id = fields.Many2one(
#         comodel_name='university.student',
#         ondelete='cascade'
        
#     )


class UniversityStudent(models.Model):
    
    _name = 'university.student'
    _inherit = ["mail.activity.mixin"]
    _rec_name = 'full_name'
    _order = 'nom asc'
    #function to set the image to default 
    @api.model
    def _default_image(self):
        image_path = get_module_resource('my_university', 'static/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())


    fields_image = fields.Image(default=_default_image)
    id = fields.Char('id')
    nom = fields.Char('Nom',
    default='',
    required=True
    )

    create_state = fields.Selection(
    [('c1','creating'),('c2','created')],'creation',
    default ='c2'
    )
    full_name=fields.Char('Fullname',
    compute='_concat_name'
    )
    prenom = fields.Char('Prenom',
    required=True,
    default=''
    )
    
    Dob = fields.Date('Date de naissance',
    required=True
    )
    sexe = fields.Selection(
            [('m','Homme'),('f','Femme')],'Sexe',required=True

        )
    cycle = fields.Selection(
        [('l1','L1'),('l2','L2'),('l3','L3'),('m1','M1'),('m2','M2')],required=True
    )


    special = fields.Selection(
        [('info','informatique'),('math','mathématique'),('isi','Ingénieurie des Sytemes'),('res','Reseaux'),('iot','IAiot')],
        'Specialité',required=True
    )

    phone = fields.Char('Telephone')
    email = fields.Char('Email')

    #many2one
    special_id=fields.Many2one(
        comodel_name='university.special',
        string = 'Spécialité',required=True
    )
    users_id = fields.Many2one(
    #fields m2o used for linking the res.users model with our model
        comodel_name='res.users',
        ondelete='cascade',
        readonly=True,
    )
    @api.constrains('Dob')
    def _check_release_date(self):
        warning('***********************\n')
        warning(timedelta(days=365*18))
        for record in self:
            
            a = fields.Date.today()-timedelta(days=365*18)
            warning(a)
            if (record.Dob>=a):
                raise models.ValidationError('you must have 18 or more'
                )
    
    
    @api.constrains('cycle','special')
    def _check_correct_special(self):
        for record in self:
            warning('******************\n')
            warning(record.special_id.cycle)
            if(record.cycle!=record.special_id.cycle):
                raise exceptions.ValidationError('you must select a correct spécialité')
    

    @api.depends('nom','prenom')
    def _concat_name(self):
        for person in self: 
            person.nom=person.nom.capitalize()
            person.prenom=person.prenom.capitalize()
            if((person.nom.isalpha()==True)and (person.prenom.isalpha()==True)):        
                person.full_name=person.nom+' '+person.prenom
            else:
                person.full_name=''

#create function already exists i override it
    @api.model
    def create(self, vals):#vals are the values entered by the user
        #creer un compte odoo lorsque un etudiant est creer
        #prend les vals sous forme de dictionnaire
        user_vals = {

                'name': str(vals["nom"]),

                'login': str(vals["email"]),

                'password': 'password',  

            }
        #creer le user id a partir des vals passer , needs sudo() to work
        user_id = self.env['res.users'].sudo().create(user_vals)
        #link between the user we created and the student
        vals["users_id"] = user_id.id
        #calling the original function then passing the vals
        student = super(UniversityStudent, self).create(vals)
        return student


    def unlink(self):
        # fonction pour supprimer un compte
        # odoo retourne true si le user est actif
        if(self.users_id):
            self.users_id.unlink()
        return super(UniversityStudent, self).unlink()

    def display_notification(self):
        # fonction pour afficher les fonctions
        title = _("Connection Test Succeeded!")
        message = _("Everything seems properly set up!")
        # le return est un dictionnaire 
        return {
            'type': 'ir.actions.save',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'sticky': False,
            }
        }


    #PRINT REPORT FUNCTION

    def action_print_report(self):
        #il n'est pas nécessaire de spécifier l'id dans la fonction report_action()
        #ref est utilisé pour acceder a l'objet creer avec l'xml
        # env represente l'envirronement  
        return self.env.ref('my_university.student_card_report').report_action(self)