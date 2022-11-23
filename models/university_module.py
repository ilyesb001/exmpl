import base64
from logging import warning
from odoo.modules.module import get_module_resource
from odoo import models,fields,api,exceptions,modules         
from datetime import datetime,timedelta

class UniversityModule(models.Model):
    _name='university.module'
    name = fields.Char('Intitulé')
    description = fields.Char('Description')
    special = fields.Many2one(
        comodel_name = 'university.special',
        string = 'Specialité'
    )