from odoo import models, fields

class SalePacking(models.Model):
    _name = 'sale.packing'
    _rec_name = 'name'

    name = fields.Char()