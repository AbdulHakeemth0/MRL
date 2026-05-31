from odoo import models, fields, _, api
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string="Task", copy=True)
    doc_created = fields.Boolean(string='Documents Created', help='Enable when other documents created')
    agent_id = fields.Many2one('res.partner', string="Agent", copy=True)
    reference_number = fields.Char(string="Reference Number",copy=True)

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
    # payment_mode = fields.Many2one('payment.mode',string="Mode of Payment")
    yard = fields.Many2one('po.yard',string="Yard", copy=True)
    delivery_term = fields.Many2one('delivery.terms', string="Delivery Term", copy=True)


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
    # def action_create_document(self):
    #     # Create the Sale Order
    #     so = self.env['sale.order'].create({
    #         'partner_id': self.env.user.partner_id.id,  # example partner
    #         'date_order': fields.Datetime.now(),
    #     })
    #     self.doc_created = True
    #
    #     # Return action to open Sale Order form
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Sale Order',
    #         'res_model': 'sale.order',
    #         'view_mode': 'form',
    #         'res_id': so.id,
    #         'target': 'current',  # use 'new' for popup
    #     }
    def action_create_sale_order(self):
        self.ensure_one()

        sale_order_vals = {
            'partner_id': self.partner_id.id,
            'origin': self.name,
            'order_line': [(0, 0, {'product_id': line.product_id.id, 'product_uom_qty': line.product_qty, 'price_unit': line.price_unit}) for line in self.order_line]
        }

        return {
            'name': 'Sale Order',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_partner_id': self.partner_id.id,
                'default_origin': self.name,
            },
        }

    def action_view_po_form(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    # def action_open_project_from_po(self):
    #     # Get all linked project IDs from selected Purchase Orders
    #     project_ids = self.mapped('project_id').ids
    #     if not project_ids:
    #         return {
    #             'type': 'ir.actions.client',
    #             'tag': 'display_notification',
    #             'params': {
    #                 'title': 'No Project linked!',
    #                 'message': 'No selected Purchase Orders have a linked Project.',
    #                 'type': 'warning',
    #                 'sticky': False,
    #             },
    #         }
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Projects',
    #         'res_model': 'project.task',
    #         'view_mode': 'form',
    #         'domain': [('id', 'in', project_ids)],
    #         'target': 'current',
    #     }

    # def action_open_po_for_project(self):
    #     # Open the PO list (can add domain/filter if needed)
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Purchase Orders',
    #         'res_model': 'purchase.order',
    #         'view_mode': 'tree,form',
    #         'target': 'current',
    #     }


    # def action_po_form(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Purchase Order',
    #         'res_model': 'purchase.order',
    #         'view_mode': 'form',
    #         'target': 'current',
    #     }

    # def action_create_document(self):
    #     admin_partner = self.env['res.partner'].search([('name', '=', 'Not defined')], limit=1)
    #     if not admin_partner:
    #         raise UserError(_("Not defined partner not found. Please create an Not defined partner in contacts."))
    #     for order in self:
    #         so_vals = {
    #             'partner_id': admin_partner.id,
    #             'task_id': order.task_id.id,
    #             'doc_created': True,
    #             'order_line': [(0, 0, {
    #                 'product_id': line.product_id.id,
    #                 'product_uom_qty': line.product_uom_qty,
    #                 'price_unit': line.price_unit,
    #                 'name': line.name,
    #                 'product_uom': line.product_uom.id,
    #
    #             }) for line in order.order_line],
    #         }
    #         self.env['sale.order'].create(so_vals)
    #     return {
    #         'effect': {
    #             'fadeout': 'slow',
    #             'message': 'Related SO Created Successfully!',
    #             'type': 'rainbow_man',
    #         }
    #     }

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    number_of_containers = fields.Char(string="No of Containers", copy=True,required=True)
    container_size = fields.Selection([
        ('20', '20 FT'),
        ('40', '40 FT')
    ], string="Container Size", required=True)
    packing_details = fields.Many2one('sale.packing',string="Packing", copy=True)
    # attachment = fields.Many2one('sale.note.attachment',string="Attachment", copy=True)
    attachment_details = fields.Many2one('sale.note.attachment',string='Attachment')


# class ProjectTask(models.Model):
#     _inherit = 'project.task'
#
#     purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')
#
#     def action_open_project_form(self):
#         project = self.env['project.project'].search([('purchase_order_id', '=', self.id)], limit=1)
#         return {
#             'type': 'ir.actions.act_window',
#             'name': 'Project',
#             'res_model': 'project.project',
#             'view_mode': 'form',
#             'res_id': project.id,
#             'target': 'current',
#         }