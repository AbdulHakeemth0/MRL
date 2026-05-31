from odoo import models, fields

class PortLoading(models.Model):
    _name = 'port.loading'
    _description = 'Port Loading'
    _rec_name = 'pl_name'

    pl_name = fields.Text(string='Port Name', required=True)