import base64
from logging import warning
from odoo.modules.module import get_module_resource
from odoo import models,fields,api,exceptions,modules         
from datetime import datetime,timedelta


class UniversityProf(models.Model):
    _name = 'university.prof'
    _rec_name = 'full_name'
    _order = 'nom asc'
    @api.model
    def _default_image(self):
        image_path = get_module_resource('my_university', 'static/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    fields_image = fields.Image(default=_default_image)
    id = fields.Char('id')
    nom = fields.Char('Nom',
    
    required=True
    )
    full_name=fields.Char('Fullname',
    compute='_concat_name'
    )
    prenom = fields.Char('Prenom',
    required=True,
    default='ilyes'
    )
    
    Dob = fields.Date('Date de naissance',
    required=True
    )
    sexe = fields.Selection(
            [('m','Homme'),('f','Femme')],'Sexe',required=True

        )

    phone = fields.Char('Telephone')
    email = fields.Char('Email')
    users_id = fields.Many2one(
        comodel_name='res.users',
        ondelete='cascade',
        readonly=True,
    )
    # #many2one
    # special_id=fields.Many2one(
    #     comodel_name='university.special',
    #     string = 'Spécialité',required=True
    # )

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


         
    @api.model
    def create(self, vals):
        
        
        user_vals = {

                'name': str(vals["nom"]),

                'login': str(vals["email"]),

                'password': 'password',  

            }
        user_id = self.env['res.users'].sudo().create(user_vals)
        vals["users_id"] = user_id.id
        student = super(UniversityProf, self).create(vals)
        return student


    def unlink(self):
        if(self.users_id):
            self.users_id.unlink()
        return super(UniversityProf, self).unlink()

