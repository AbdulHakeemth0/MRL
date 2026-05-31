from odoo import models, fields

class LoadingTime(models.Model):
    _name = 'loading.time'
    _description = 'Loading Time'
    _rec_name = 'lt_name'

    lt_name = fields.Char(string='Loading Time', required=True)