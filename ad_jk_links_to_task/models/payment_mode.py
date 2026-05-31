from odoo import models, fields

class PaymentMode(models.Model):
    _name = 'payment.mode'
    _rec_name = 'pm_name'

    pm_name = fields.Char(sting='Payment Mode')