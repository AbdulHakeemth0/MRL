from odoo import api, models, fields, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    advance_amount = fields.Monetary(
        string="Advance Amount",
        currency_field="currency_id",
        help="Advance amount received from the customer."
    )
    currency_id = fields.Many2one('res.currency', string='Currency')
    # currency_id = fields.Many2one(
    #     'res.currency',
    #     string="Currency",
    #     related='company_id.currency_id',
    # )
    task_id = fields.Many2one('project.task', string="Task")
    agent_id = fields.Many2one('res.partner', string="Agent", copy=True)
    ref_no = fields.Char(string="Reference No",copy=True)
    doc_created = fields.Boolean(string='Documents Created', help='Enable when other documents created')
    related_doc_ids = fields.One2many('inv.related.doc', 'sale_id', string='Related Documents')
    partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string="Customer Bank",
        domain="[('partner_id', '=', partner_id)]",
        help="Customer bank details"
    )

    company_partner_id = fields.Many2one(
        'res.partner',
        related="company_id.partner_id",
        store=True
    )
    company_bank_id = fields.Many2one(
        'res.partner.bank',
        string="Company Bank",
        domain="[('partner_id', '=', company_partner_id)]",
        help="Customer bank details"
    )
    port_of_ids = fields.Many2one('port.loading',string='Port of Loading', copy=True)
    discharge_ids = fields.Many2one('port.discharge',string='Port of Discharge', copy=True)
    final_ids = fields.Many2one('final.destination',string='Final Destination', copy=True)
    delivery_ids = fields.Many2one('delivery.terms',string='Delivery Terms', copy=True)

    @api.onchange('partner_id')
    def _onchange_partner_id_set_bank(self):
        for order in self:
            if order.partner_id:
                # Automatically select the first bank account if available
                banks = self.env['res.partner.bank']
                bank_accounts = banks.search([('partner_id', '=', order.partner_id.id)])
                order.partner_bank_id = bank_accounts[:1] if bank_accounts else False
                company_bank_accounts = banks.search([('partner_id', '=', order.company_partner_id.id)])
                order.company_bank_id = company_bank_accounts[:1] if company_bank_accounts else False
    def action_create_purchase_order(self):
        self.ensure_one()  # Ensure only one sale order is selected

        # Prepare default values for purchase order
        purchase_order_vals = {
            'partner_id': self.partner_id.id,  # supplier/customer
            'origin': self.name,               # reference from Sale Order
            # Add more fields if needed
        }

        # Open Purchase Order form
        return {
            'name': 'Purchase Order',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'target': 'current',  # 'new' for popup
            'context': {
                'default_partner_id': self.partner_id.id,
                'default_origin': self.name,
            },
        }


        # def action_create_document_po(self):
    #     # Create the Sale Order
    #     po = self.env['purchase.order'].create({
    #         'partner_id': self.env.user.partner_id.id,
    #         'date_order': fields.Datetime.now(),
    #     })
    #     self.doc_created = True
    #
    #     # Return action to open Sale Order form
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Purchase Order',
    #         'res_model': 'purchase.order',
    #         'view_mode': 'form',
    #         'res_id': po,
    #         'target': 'current',  # use 'new' for popup
    #     }

    # def action_create_document(self):
    #
    # # Create Purchase Order
    #     po = self.env['purchase.order'].create({
    #          'partner_id': self.env.user.partner_id.id,
    #          'date_order': fields.Date.today(),
    #          'company_id': self.env.company.id,
    #     })
    #
    # # Return action to open PO form
    #     return {
    #        'type': 'ir.actions.act_window',
    #         'name': 'Purchase Order',
    #         'res_model': 'purchase.order',
    #          'view_mode': 'form',
    #           'res_id': po.id,
    #           'target': 'current',   # open in the same window
    #     }
        def action_create_document(self):
        # Create Purchase Order
            po = self.env['purchase.order'].create({
                'partner_id': self.env.user.partner_id.id,
                'date_order': fields.Date.today(),
                'company_id': self.env.company.id,
            })

            # Return action to open PO form
            return {
                'type': 'ir.actions.act_window',
                'name': 'Purchase Order',
                'res_model': 'purchase.order',
                'view_mode': 'form',
                'res_id': po.id,
                'target': 'current',   # open in the same window
            }
    # def action_create_document(self):
    #     admin_partner = self.env['res.partner'].search([('name', '=', 'Not defined')], limit=1)
    #     if not admin_partner:
    #         raise UserError(_("Not defined partner not found. Please create an Not defined partner in contacts."))
    #     for order in self:
    #         po_vals = {
    #             'partner_id': admin_partner.id,
    #             'task_id': order.task_id.id,
    #             'doc_created': True,
    #             'order_line': [(0, 0, {
    #                 'product_id': line.product_id.id,
    #                 'product_qty': line.product_uom_qty,
    #                 'price_unit': line.price_unit,
    #                 'name': line.name,
    #                 'product_uom': line.product_uom.id,
    #             }) for line in order.order_line],
    #         }
    #         self.env['purchase.order'].create(po_vals)
    #     return {
    #         'effect': {
    #             'fadeout': 'slow',
    #             'message': 'Related PO Created Successfully!',
    #             'type': 'rainbow_man',
    #         }
    #     }

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()

        invoice_vals.update({
        # port loading names
        'port_of_loading': ', '.join(self.port_of_ids.mapped('pl_name')) if self.port_of_ids else '',

        # port discharge names
        'discharge_of_port': ', '.join(self.discharge_ids.mapped('pd_name')) if self.discharge_ids else '',

        # port final destination names
        'final_destination': ', '.join(self.final_ids.mapped('fd_name')) if self.final_ids else '',

        # delivery terms (SaleOrder.delivery_ids → Invoice.freight_term)
        'freight_term': ', '.join(self.delivery_ids.mapped('dt_name')) if self.delivery_ids else '',

        # packing
        'packing': self.order_line[0].packing.name
        if self.order_line and self.order_line[0].packing else '',

        # product chemical elements
        'chemical_elements_present': (
            self.order_line[0].product_id.chemical_elements_present
            if self.order_line else ''
        ),
        })
        return invoice_vals

class InvRelatedDoc(models.Model):
    "For storing the records created from Invoice of the sale order."
    _name = 'inv.related.doc'

    sale_id = fields.Many2one('sale.order')
    invoice_id = fields.Many2one('account.move')
    packing_list_id = fields.Many2one('packing.list')
    analysis_id = fields.Many2one('certificate.analysis')
    origin_id = fields.Many2one('certificate.origin')
    freight_id = fields.Many2one('freight.certificate')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    container_qty = fields.Char(string='No of Containers', copy=True)
    packing = fields.Many2one('sale.packing',string='Packing', copy=True)
    # attachment = fields.Many2one('sale.note.attachment',string='Attachment')
    attachment_note = fields.Many2one('sale.note.attachment', string='Attachment Note', store=True, copy=True)
    # advance_amount = fields.Monetary(
    #     string="Advance Amount",
    #     currency_field="currency_id",
    # )
    # @api.depends('order_line.price_total', 'order_line.price_tax', 'advance_amount')
    # def _compute_amount(self):
    #     """Override total computation to include advance amount deduction."""
    #     for order in self:
    #         # Compute totals from order lines
    #         amount_untaxed = sum(line.price_subtotal for line in order.order_line)
    #         amount_tax = sum(line.price_tax for line in order.order_line)
    #         advance = order.advance_amount or 0.0
    #
    #         currency = order.currency_id or order.company_id.currency_id
    #         order.amount_untaxed = currency.round(amount_untaxed)
    #         order.amount_tax = currency.round(amount_tax)
    #         order.amount_total = currency.round(amount_untaxed + amount_tax - advance)


    #

class SaleNoteAttachment(models.Model):
    _name = 'sale.note.attachment'
    _description = 'Sale Order Note Attachment'
    _rec_name = 'note'

    note = fields.Char(string='Description')