from logging import warning
from odoo.exceptions import UserError
from odoo import models,fields,api

class UniversitySpecial(models.Model):
    _name='university.special'
    _description='university levels and specialities'
    name =fields.Char('name')
    _rec_name='special_s'
    cycle = fields.Selection(
        [('l1','L1'),('l2','L2'),('l3','L3'),('m1','M1'),('m2','M2')],
        required=True
    )

    special_s = fields.Selection(
        [('informatique','informatique'),('mathématique','mathématique'),('Ingénieurie des Sytemes','Ingénieurie des Sytemes'),('Reseaux','Reseaux'),('IAiot','IAiot')],
        'Specialité',
        required=True
    )
    
    # _sql_constraints = [
    #     ("cycle_uniq","UNIQUE(name)" ,"name already exists")
    # ]

    @api.constrains('cycle','special_s')
    def _check_dupli(self):
        
        rec_special = self.env['university.special'].search([('cycle','=',self.cycle),('special_s','=',self.special_s),('id','!=',self.id)])
        warning(rec_special)
        if rec_special:
            raise models.ValidationError('"' + self.special_s + '" is already in Odoo!')
