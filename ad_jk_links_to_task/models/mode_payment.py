from odoo import models, fields

class ModePayment(models.Model):
    _name = 'mode.payment'
    _description = 'Mode Payment'
    _rec_name = 'm_name'

    m_name = fields.Char(string='Mode Payment', required=True)