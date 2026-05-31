from odoo import models, fields, api
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    name = fields.Char(
        string='Order Reference',
        copy=False,
        readonly=True,
        index=True,
        default='New'
    )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('sale.order.mrl_llc')
            vals['name'] = sequence or 'New'
        return super(SaleOrder, self).create(vals)

    def _create_invoices(self, grouped=False, final=False):
        invoices = super()._create_invoices(grouped=grouped, final=final)

        for order in self:
            for invoice in invoices.filtered(lambda m: m.invoice_origin == order.name):

                invoice_lines = []

                for so_line in order.order_line:
                    if so_line.display_type:
                        continue

                    vals = {
                        'move_id': invoice.id,
                        'product_id': so_line.product_id.id,
                        'name': so_line.name,
                        'quantity': so_line.product_uom_qty,
                        'price_unit': so_line.price_unit,
                        'tax_ids': [(6, 0, so_line.tax_id.ids)],
                        'product_uom_id': so_line.product_uom.id,
                        'gross_weight': so_line.gross_weight,
                        'net_weight': so_line.net_weight,
                        'container_no': so_line.container_no,
                        'hsn_code': so_line.product_id.hsn_code,
                        'sale_line_ids': [(6, 0, [so_line.id])],
                    }

                    invoice_lines.append((0, 0, vals))

                # remove auto lines and replace with SO lines
                invoice.invoice_line_ids.unlink()
                invoice.write({'invoice_line_ids': invoice_lines})

        return invoices


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    name = fields.Char(
        string="Purchase Order",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('purchase.order.mrl_llc')
    )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order.mrl_llc')
        return super(PurchaseOrder, self).create(vals)




class AccountMove(models.Model):
    _inherit = 'account.move'

    name = fields.Char(string='Invoice Number',  copy=False, readonly=True,
                       index=True, default=lambda self: 'New')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New' and vals.get('move_type') in ('out_invoice', 'in_invoice'):
            vals['name'] = self.env['ir.sequence'].next_by_code('account.move.mrl_llc')
        return super(AccountMove, self).create(vals)