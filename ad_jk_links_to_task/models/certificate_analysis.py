from odoo import models, fields, api, _


class CertificateAnalysis(models.Model):
    _name = 'certificate.analysis'
    _rec_name = 'number'
    _description = 'Certificate of Analysis'

    number = fields.Char("Reference", default=lambda self: _('New'),
                         copy=False, readonly=True, tracking=True, store=True)
    consignee_info_id = fields.Many2one('res.partner', string='Consignee/Notify Party')
    material_description = fields.Char(string='Material Description')
    container_no = fields.Char(string='Container No')
    seal_no = fields.Char(string='Seal No')
    bill_of_lading_no = fields.Char(string='Bill of Lading No')
    shipped_on_board = fields.Date(string='Shipped on Board Date')
    vessel_name = fields.Char(string='Vessel Name')
    voyage_no = fields.Char(string='Voyage No')
    port_of_loading = fields.Char(string='Port of Loading')
    discharge_of_port = fields.Char(string='Port of Discharge')
    final_destination = fields.Char(string='Final Destination')
    invoice_no = fields.Char(string='Invoice No')
    invoice_date = fields.Date(string='Invoice Date')
    contract_no = fields.Char(string='Contract No')
    contract_date = fields.Date(string='Contract Date')
    packing = fields.Char(string='Packing')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )


    # New field for chemical composition
    chemical_elements_present = fields.Html(string='Chemical Elements Present')
    task_id = fields.Many2one('project.task', string="Task")

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the analysis model """
        for vals in vals_list:
            if vals.get('number', _('New')) == _('New'):
                vals['number'] = (self.env['ir.sequence'].
                                  next_by_code('certificate.analysis'))
        return super().create(vals_list)
