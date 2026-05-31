from odoo import fields, models, api, _


class FreightCertificate(models.Model):
    _rec_name = 'number'
    _name = 'freight.certificate'

    number = fields.Char("Reference", default=lambda self: _('New'),
                         copy=False, readonly=True, tracking=True, store=True)
    material_description = fields.Char()
    bill_of_loading_no = fields.Char()
    vessel_name = fields.Char()
    ocean_freight = fields.Float(string="Ocean Freight",
        digits=(16, 2)
    )
    shipped_on_board = fields.Date()
    voyage_no = fields.Char()

    shipper = fields.Many2one('res.partner')
    # contact_no = fields.Char()
    # email = fields.Char()

    consignee = fields.Many2one('res.partner')
    # consignee_gst = fields.Char(string='GST')
    # consignee_pan = fields.Char(string='Pan No')
    # consignee_iec_code = fields.Char(string='IEC Code')
    # consignee_contact = fields.Char(string='Contact')
    # consignee_no = fields.Char(string='Contact No')
    # consignee_email = fields.Char(string='Email')

    task_id = fields.Many2one('project.task', string="Task")
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the analysis model """
        for vals in vals_list:
            if vals.get('number', _('New')) == _('New'):
                vals['number'] = (self.env['ir.sequence'].
                                  next_by_code('freight.certificate'))
        return super().create(vals_list)
