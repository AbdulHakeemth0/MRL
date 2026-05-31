from odoo import models, fields

class PoYard(models.Model):
    _name = 'po.yard'
    _rec_name = 'name'

    name = fields.Char()