from odoo import models, fields

class PortDischarge(models.Model):
    _name = 'port.discharge'
    _description = 'Port of Discharge'
    _rec_name = 'pd_name'

    pd_name = fields.Char(string="Port of Discharge", required=True)