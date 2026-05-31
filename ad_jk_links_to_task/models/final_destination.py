from odoo import models, fields

class FinalDestination(models.Model):
    _name = 'final.destination'
    _description = 'Final Destination'
    _rec_name = 'fd_name'

    fd_name = fields.Char(string="Final Destination")