# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    iec_code = fields.Char(string='IEC Code', size=10)
    currency_id = fields.Many2one('res.currency', string='Currency')
    pan_no = fields.Char(string='PAN No')
    contact_person_id = fields.Many2one('res.partner')
    cr_number = fields.Char(string='CR NO')

    @api.constrains('iec_code')
    def _check_iec_code_length(self):
        for record in self:
            if record.iec_code and len(record.iec_code) != 10:
                raise ValidationError("IEC Code must be exactly 10 digits long.")


class ResBank(models.Model):
    _inherit = 'res.bank'


    iban_code = fields.Char(string='IBAN Code')

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    iban_code = fields.Char(string="IBAN", copy=True)
    # iban= fields.Char(string="IBAN", copy=True)

class ResBank(models.Model):
    _inherit = 'res.bank'

    iban = fields.Char(string='IBAN')


    # def _compute_iban(self):
    #     for rec in self:
    #         rec.iban_code = rec.iban_code or ''


