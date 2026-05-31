from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    signature_stamp_1 = fields.Binary(string="Signature / Stamp LLC")
    signature_stamp_2 = fields.Binary(string="Signature / Stamp FZC")
    # signature = fields.Binary(string="Signature")
    show_signature_stamp_1 = fields.Boolean(
        string='Show Signature Stamp LLC',
        default=False,
        help='Enable to display signature stamp on reports'
    )
    show_signature_stamp_2 = fields.Boolean(
        string='Show Signature Stamp FZC',
        default=False,
        help='Enable to display signature stamp on reports'
    )

    @api.model
    def _update_signature_stamp_by_name(self, company_name):
        """Update signature stamp visibility for specific company"""
        company = self.search([('name', '=', company_name)], limit=1)
        if company:
            company.write({'show_signature_stamp_1': True})
            company.write({'show_signature_stamp_2': True})
        return True

