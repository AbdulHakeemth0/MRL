# -*- coding: utf-8 -*-
from odoo import models, fields,api


class AccountMoveLine(models.Model):
    """Inheriting the account move line for adding the date fields"""
    _inherit = 'account.move.line'

    container_no = fields.Char(string='Container No')
    gross_weight = fields.Float(string='Gross Weight(MT)', digits=(16, 3))
    net_weight = fields.Float(string='Net Weight(MT)', digits=(16, 3))
    seal_numbers = fields.Char(string='Seal Number(s)')
    down_payment_percent = fields.Float(string="Down Payment %")

    @api.depends('net_weight', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.price_subtotal = (line.net_weight or 0.0) * (line.price_unit or 0.0)

    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute="_compute_subtotal",
        store=True,
        currency_field='currency_id',
    )



class AccountMove(models.Model):
    _inherit = 'account.move'

    seal_numbers = fields.Char(string='Seal Number(s)')
    advance_percent = fields.Float(string="Advance %")
    advance_amount = fields.Float(
        string="Advance Amount",
        store=True
    )

    @api.depends('advance_percent', 'invoice_line_ids.price_subtotal')
    def _compute_advance_amount(self):
        for rec in self:
            total_subtotal = sum(rec.invoice_line_ids.mapped('price_subtotal'))
            rec.advance_amount = total_subtotal * (rec.advance_percent / 100.0) if rec.advance_percent else 0.0

    def _jk_get_proforma_report_lines(self):
        self.ensure_one()
        report_lines = []

        for line in self.invoice_line_ids.filtered(lambda l: not l.display_type or l.display_type == 'product'):
            product_name = (line.product_id.name or line.name or '').strip()

            sale_line = line.sale_line_ids[:1]
            report_lines.append({
                'product_name': product_name,
                'product_uom_qty': line.quantity or 0.0,
                'hsn_code': getattr(line.product_id, 'hsn_code', False) or '',
                'container_qty': getattr(sale_line, 'container_qty', False) or getattr(line, 'container_qty', False) or 0.0,
                'packing': getattr(getattr(sale_line, 'packing', False), 'name', False) or '',
                'gross_weight': line.gross_weight or 0.0,
                'net_weight': line.net_weight or 0.0,
                'price_unit': line.price_unit or 0.0,
                'price_subtotal': line.price_subtotal or 0.0,
            })

        return report_lines

    def _jk_get_proforma_logistics(self):
        self.ensure_one()
        return {
            'port_of_loading': getattr(self, 'port_of_loading', False) or '-',
            'port_of_discharge': getattr(self, 'discharge_of_port', False) or '-',
            'final_destination': getattr(self, 'final_destination', False) or '-',
            'delivery_terms': getattr(self, 'freight_term', False) or '',
            'packing': getattr(self, 'packing', False) or '-',
        }

    def _jk_get_partner_bank_details(self):
        self.ensure_one()
        bank = getattr(self, 'partner_bank_id', False)
        bank_record = getattr(bank, 'bank_id', False) if bank else False
        return {
            'bank_name': getattr(bank, 'bank_name', False) or '',
            'street': getattr(bank_record, 'street', False) or '',
            'account_no': getattr(bank, 'acc_number', False) or '',
            'swift': getattr(bank_record, 'bic', False) or '',
            'iban': getattr(bank, 'iban_code', False) or '',
            'contact_no': getattr(bank, 'contact_number', False) or '',
        }

    def _jk_get_proforma_payment_terms(self):
        self.ensure_one()
        date_ref = self.invoice_date or fields.Date.context_today(self)
        amount_untaxed = self.amount_untaxed or 0.0
        amount_tax = self.amount_tax or 0.0

        if not self.invoice_payment_term_id:
            return [{
                'label': 'Due Amount',
                'date': date_ref,
                'amount': self.amount_total or 0.0,
            }]

        terms = self.invoice_payment_term_id._compute_terms(
            date_ref=date_ref,
            currency=self.currency_id,
            company=self.company_id,
            tax_amount=amount_tax,
            tax_amount_currency=amount_tax,
            sign=1,
            untaxed_amount=amount_untaxed,
            untaxed_amount_currency=amount_untaxed,
        )
        term_lines = self.invoice_payment_term_id.line_ids
        values = []
        for index, term in enumerate(terms['line_ids']):
            payment_line = term_lines[index] if index < len(term_lines) else False
            if payment_line and payment_line.value == 'percent':
                label = '%.2f%% Payment' % payment_line.value_amount
            elif payment_line and payment_line.value == 'fixed':
                label = 'Fixed Payment'
            else:
                label = 'Balance Payment'
            values.append({
                'label': label,
                'date': term['date'],
                'amount': term['foreign_amount'],
            })
        return values


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        action = super().create_invoices()

        # Get created invoices
        if isinstance(action, dict) and action.get('res_id'):
            invoices = self.env['account.move'].browse(action['res_id'])
        elif isinstance(action, dict) and action.get('domain'):
            invoices = self.env['account.move'].search(action['domain'])
        else:
            invoices = self.env['account.move']

        for invoice in invoices:
            for line in invoice.invoice_line_ids:
                # Link back to sale order line
                so_line = line.sale_line_ids[:1]
                if so_line:
                    line.write({
                        'net_weight': so_line.net_weight,
                        'gross_weight': so_line.gross_weight,
                    })

        return action

