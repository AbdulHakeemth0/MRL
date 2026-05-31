from odoo import models, fields

class DeliveryTerms(models.Model):
    _name = 'delivery.terms'
    _description = 'Delivery Terms'
    _rec_name = 'dt_name'

    dt_name = fields.Char(string="Delivery Term", required=True)
