from odoo import api, fields, models,_


class PackingList(models.Model):
    _name = 'packing.list'
    _rec_name = 'number'

    number = fields.Char("Reference", default=lambda self: _('New'),
                         copy=False, readonly=True, tracking=True)
    partner_id = fields.Many2one('res.partner')
    # gstin = fields.Char()
    # pan_no = fields.Char()
    # iec_code = fields.Char()
    # contact_person_id = fields.Many2one('res.partner')
    # contact_no = fields.Char()
    # email_id = fields.Char()
    invoice_no = fields.Char()
    invoice_date = fields.Date()
    contract_no = fields.Char()
    contract_date = fields.Date()


    bill_of_loading_no = fields.Char()
    vessel_name = fields.Char()
    port_of_loading = fields.Char()
    final_destination = fields.Char()

    shipped_on_board = fields.Date()
    voyage_no = fields.Char()
    discharge_of_port = fields.Char()
    packing_type = fields.Char()

    material_ids = fields.One2many('packing.material', 'packing_id')

    task_id = fields.Many2one('project.task', string="Task")
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the student model """
        for vals in vals_list:
            if vals.get('number', _('New')) == _('New'):
                vals['number'] = (self.env['ir.sequence'].
                                  next_by_code('packing.list'))
        return super().create(vals_list)


class PackingMaterial(models.Model):
    _name = 'packing.material'

    packing_id = fields.Many2one('packing.list')
    sl_no = fields.Integer()
    product_id = fields.Many2one('product.product')
    hsn_code = fields.Char()
    container_no = fields.Char()
    seal_no = fields.Char()
    gross_weight = fields.Float(digits=(16,3))
    tare_weight = fields.Float(digits=(16,3))
    net_weight = fields.Float(digits=(16,3))







