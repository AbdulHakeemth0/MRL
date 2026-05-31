# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    gross_weight = fields.Float(string='Gross Weight(MT)', digits=(16, 2))
    net_weight = fields.Float(string='Net Weight(MT)', digits=(16, 2))

    @api.onchange('net_weight')
    def _onchange_net_weight(self):
        for line in self:
            line.product_uom_qty = line.net_weight


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _jk_get_proforma_report_lines(self):
        self.ensure_one()
        report_lines = []

        for line in self.order_line.filtered(lambda l: not l.display_type):
            product_name = (line.product_id.name or line.name or '').strip()

            # Skip down payment
            if product_name.lower() == 'down payment':
                continue

            report_lines.append({
                'product_name': product_name,
                'product_uom_qty': line.product_uom_qty or 0.0,  # ✅ REQUIRED
                'hsn_code': getattr(line.product_id, 'hsn_code', False) or '',
                'container_qty': getattr(line, 'container_qty', False) or 0.0,  # ✅ FIXED NAME
                'packing': getattr(getattr(line, 'packing', False), 'name', False) or '',
                'gross_weight': line.gross_weight or 0.0,
                'net_weight': line.net_weight or 0.0,
                'price_unit': line.price_unit or 0.0,
                'price_subtotal': line.price_subtotal or 0.0,
            })

        return report_lines

    def _jk_get_proforma_logistics(self):
        self.ensure_one()
        first_line = self.order_line[:1]
        port = getattr(getattr(self, 'port_of_ids', False), 'pl_name', False)
        discharge = getattr(getattr(self, 'discharge_ids', False), 'pd_name', False)
        final_destination = getattr(getattr(self, 'final_ids', False), 'fd_name', False)
        delivery = getattr(getattr(self, 'delivery_ids', False), 'dt_name', False)
        packing = getattr(getattr(first_line, 'packing', False), 'name', False) if first_line else False
        return {
            'port_of_loading': port or '-',
            'port_of_discharge': discharge or '-',
            'final_destination': final_destination or '-',
            'delivery_terms': delivery or '',
            'packing': packing or '-',
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
        date_ref = self.date_order.date() if self.date_order else fields.Date.context_today(self)
        amount_untaxed = self.amount_untaxed or 0.0
        amount_tax = self.amount_tax or 0.0

        if not self.payment_term_id:
            return [{
                'label': 'Due Amount',
                'date': date_ref,
                'amount': self.amount_total or 0.0,
            }]

        terms = self.payment_term_id._compute_terms(
            date_ref=date_ref,
            currency=self.currency_id,
            company=self.company_id,
            tax_amount=amount_tax,
            tax_amount_currency=amount_tax,
            sign=1,
            untaxed_amount=amount_untaxed,
            untaxed_amount_currency=amount_untaxed,
        )
        term_lines = self.payment_term_id.line_ids
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
