from odoo import models, fields, _,api
from odoo.fields import Command
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    task_id = fields.Many2one('project.task', string="Task", copy=True)
    doc_created = fields.Boolean(string='Documents Created', help='Enable when other documents created')

    container_no = fields.Char(string='Container No', copy=True)
    bill_of_lading_no = fields.Char(string='Bill of Loading No')
    shipped_on_board = fields.Date(string='Shipped on Board Date')
    vessel_name = fields.Char(string='Vessel Name')
    voyage_no = fields.Char(string='Voyage No')
    port_of_loading = fields.Char(string='Port of Loading', copy=True)
    discharge_of_port = fields.Char(string='Port of Discharge', copy=True)
    final_destination = fields.Char(string='Final Destination', copy=True)
    packing = fields.Char(string='Packing', copy=True)
    freight_term = fields.Char(string='Freight Term', copy=True)

    chemical_elements_present = fields.Text(string='Chemical Elements Present', copy=True)
    seal_no = fields.Char(string='Seal No', copy=True)

    ocean_freight = fields.Float(string="Ocean Freight", copy=True)

    partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string="Customer Bank",
        domain="[('partner_id', '=', partner_id)]",
        help="Customer bank details"
    )

    @api.onchange('partner_id')
    def _onchange_partner_id_set_bank(self):
        for order in self:
            if order.partner_id:
                # Automatically select the first bank account if available
                bank_accounts = self.env['res.partner.bank'].search([('partner_id', '=', order.partner_id.id)])
                order.partner_bank_id = bank_accounts[:1] if bank_accounts else False

    def action_create_document(self):
        admin_partner = self.env['res.partner'].search([('name', '=', 'Not defined')], limit=1)
        sale_order = self.env['sale.order'].search([('invoice_ids', '=', self.id)], limit=1)
        if not admin_partner:
            raise UserError(_("Not defined partner not found. Please create an Not defined partner in contacts."))
        pl_vals = {
            'partner_id': self.partner_id.id,
            'task_id': sale_order.task_id.id,
            'invoice_no': self.name,
            'invoice_date': self.invoice_date,
            'contract_no': sale_order.name,
            'contract_date': sale_order.date_order,
            'bill_of_loading_no': self.bill_of_lading_no,
            'vessel_name': self.vessel_name,
            'port_of_loading': self.port_of_loading,
            'final_destination': self.final_destination,
            'shipped_on_board': self.shipped_on_board,
            'voyage_no': self.voyage_no,
            'discharge_of_port': self.discharge_of_port,
            'packing_type': self.packing,
            'material_ids': [(0, 0, {
                'sl_no': index + 1,
                'product_id': line.product_id.id,
                'hsn_code': line.product_id.hsn_code,
                'container_no': line.container_no,
                'seal_no': line.seal_numbers,
                'gross_weight': line.gross_weight,
                'net_weight': line.net_weight,
            }) for index, line in enumerate(self.invoice_line_ids)],
        }
        packing_list = self.env['packing.list'].create(pl_vals)
        coa_vals = {
            'consignee_info_id': self.partner_id.id,
            'task_id': sale_order.task_id.id,
            'material_description': self.line_ids[0].product_id.name,
            'invoice_no': self.name,
            'invoice_date': self.invoice_date,
            'contract_no': sale_order.name,
            'contract_date': sale_order.date_order,
            'container_no': '-'.join(str(line.container_no) for line in self.invoice_line_ids),
            'seal_no': '-'.join(str(line.seal_numbers) for line in self.invoice_line_ids),
            'bill_of_lading_no': self.bill_of_lading_no,
            'shipped_on_board': self.shipped_on_board,
            'vessel_name': self.vessel_name,
            'voyage_no': self.voyage_no,
            'port_of_loading': self.port_of_loading,
            'discharge_of_port': self.discharge_of_port,
            'final_destination': self.final_destination,
            'packing': self.packing,
            'chemical_elements_present': self.chemical_elements_present,
        }
        analysis = self.env['certificate.analysis'].create(coa_vals)
        certificate_text = (
            f"This is to certify that the goods loaded in the container {self.container_no} "
            f"belongs to our Invoice No {self.name} and are of {self.port_of_loading} Origin."
            f"We also certify that this material does not contain any spent and unspent war radioactive materials and it is free from any form of arms, ammunitions, and explosives."
        )
        origin_vals = {
            'consignee_info_id': self.partner_id.id,
            'task_id': sale_order.task_id.id,
            'invoice_no': self.name,
            'invoice_date': self.invoice_date,
            'contract_no': sale_order.name,
            'contract_date': sale_order.date_order,
            'certification_text': certificate_text,
        }
        origin = self.env['certificate.origin'].create(origin_vals)
        freight_vals = {
            'consignee': self.partner_id.id,
            'shipper': self.company_id.partner_id.id,
            'task_id': sale_order.task_id.id,
            'material_description': self.line_ids[0].product_id.name,
            'bill_of_loading_no': self.bill_of_lading_no,
            'vessel_name': self.vessel_name,
            'ocean_freight': self.ocean_freight,
            'shipped_on_board': self.shipped_on_board,
            'voyage_no': self.voyage_no,
        }
        freight = self.env['freight.certificate'].create(freight_vals)
        sale_order.related_doc_ids = [Command.create({'sale_id': sale_order.id,
                                                      'invoice_id': self.id,
                                                      'packing_list_id': packing_list.id,
                                                      'analysis_id': analysis.id,
                                                      'origin_id': origin.id,
                                                      'freight_id': freight.id,
                                                      })]
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Related Documents created successfully!',
                'type': 'rainbow_man',
            }
        }
