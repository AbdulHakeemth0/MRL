from odoo import models, fields

class ResBank(models.Model):
    _inherit = 'res.bank'

    # contact_person = fields.Many2one('res.partner', string='Contact Person')
    # contact_number = fields.Char(string='Contact Number')
    ifsc_code = fields.Char(string='IFSC Code', copy=True)
    # iban_code = fields.Char(string='IBAN Code')
    branch = fields.Char(string='Branch', copy=True)
    po_box = fields.Char(string='PO Box', copy=True)
    corre_bank = fields.Many2one('res.bank',string='Correspondence Bank')
class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    contact_person = fields.Many2one('res.partner', string='Contact Person', copy=True)
    contact_number = fields.Char(string='Contact Number', copy=True)
    account_type = fields.Selection([
        ('current', 'Current'),
        ('saving', 'Saving'),
        ('commercial premium current acct', 'Commercial Premium Current Acct'),
    ], string="Account Type")
    swift = fields.Char(string='SWIFT')
    # account_type = fields.Selection([
    #     ('Current', 'Current'),
    #     ('Saving', 'Saving'),
    # ], string="Account Type")
    branch = fields.Char(string='Branch', copy=True)
    po_box = fields.Char(string='PO Box', copy=True)
    address = fields.Char(string='Address', copy=True)
    corre_bank = fields.Many2one('res.bank', string='Correspondance Bank', copy=True)


