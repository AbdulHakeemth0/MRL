from odoo import api, models, fields, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    hsn_code = fields.Char(string='HSN Code', copy=True)
    chemical_elements_present = fields.Html(string='Chemical Elements Present', copy=True)