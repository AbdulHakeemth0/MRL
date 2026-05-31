from odoo import models, fields, api, _

class CertificateOfOrigin(models.Model):
    _name = 'certificate.origin'
    _rec_name = 'number'
    _description = 'Certificate of Origin'



    # invoice_id = fields.Many2one('account.move', string='Invoice')
    #
    # # Related fields to pull data from the linked invoice
    # # port_of_loading = fields.Char(related='invoice_id.port_of_loading', string='Port of Loading', store=False)
    # # invoice_no = fields.Char(related='invoice_id.name', string='Invoice No', store=False)
    # container_no = fields.Char(related='invoice_id.invoice_line_ids.container_no', string='Container No', store=False)

    number = fields.Char("Reference", default=lambda self: _('New'),
                         copy=False, readonly=True, tracking=True, store=True)

    consignee_info_id = fields.Many2one('res.partner', string='Consignee/Notify Party')
    # invoice_no = fields.Many2one('account.move',string='Invoice No')
    invoice_date = fields.Date(string='Invoice Date', copy=True, store=True)
    contract_no = fields.Char(string='Contract No')
    contract_date = fields.Date(string='Contract Date')

    certification_text = fields.Text(string='Certification Text')
    task_id = fields.Many2one('project.task', string="Task")
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )
    invoice_id = fields.Many2one('account.move', string='Invoice', domain=[('move_type', '=', 'out_invoice')])
    invoice_no = fields.Char(string='Invoice No')
    port_of_loading = fields.Char(string='Port of Loading',)
    container_no = fields.Char(string='Container No',)

    @api.onchange('invoice_id')
    def _onchange_invoice_id(self):
        for rec in self:
            if rec.invoice_id:
                inv = rec.invoice_id

                rec.invoice_no = inv.name
                rec.invoice_date = inv.invoice_date
                rec.port_of_loading = inv.port_of_loading

                # Collect all container numbers from invoice lines
                containers = inv.invoice_line_ids.mapped('container_no')

                # Remove empty values and join as list
                containers = list(filter(None, containers))

                rec.container_no = ', '.join(containers) if containers else False
            else:
                rec.invoice_no = False
                rec.invoice_date = False
                rec.port_of_loading = False
                rec.container_no = False

    # @api.onchange('invoice_id')
    # def _onchange_invoice_id(self):
    #     for rec in self:
    #         if rec.invoice_id:
    #             rec.invoice_no = rec.invoice_id.name or ''
    #             rec.invoice_date = rec.invoice_id.invoice_date  # <-- Auto-fill Invoice Date
    #             rec.port_of_loading = rec.invoice_id.port_of_loading or ''
    #
    #             # Take first invoice line as example for container_no
    #             line = rec.invoice_id.invoice_line_ids[:1]
    #             rec.container_no = line.container_no if line else ''
    #         else:
    #             rec.invoice_no = ''
    #             rec.invoice_date = False
    #             rec.port_of_loading = ''
    #             rec.container_no = ''



    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the analysis model """
        for vals in vals_list:
            if vals.get('number', _('New')) == _('New'):
                vals['number'] = (self.env['ir.sequence'].
                                  next_by_code('certificate.origin'))
        return super().create(vals_list)


