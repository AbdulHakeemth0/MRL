from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    sale_order_ids = fields.One2many('sale.order', 'task_id', string="Sale Orders")
    purchase_order_ids = fields.One2many('purchase.order', 'task_id', string="Purchase Orders")
    certificate_origin_ids = fields.One2many('certificate.origin', 'task_id', string="Certificate Origin")
    certificate_analysis_ids = fields.One2many('certificate.analysis', 'task_id', string="Certificate Analysis")

    sale_order_count = fields.Integer(string="Sale Order Count", compute="_compute_sale_order_count")
    purchase_order_count = fields.Integer(string="Purchase Order Count", compute="_compute_purchase_order_count")
    certificate_origin_count = fields.Integer(string="Certificate Origin Count",
                                              compute="_compute_certificate_origin_count")
    certificate_analysis_count = fields.Integer(string="Certificate Analysis Count",
                                              compute="_compute_certificate_analysis_count")
    packing_list_count = fields.Integer(string='Packing List Count', compute='_compute_packing_list_count')
    packing_list_ids = fields.One2many('packing.list', 'task_id', string='Packing List')

    freight_certificate_count = fields.Integer(string='Freight Certificate',
                                               compute='_compute_freight_certificate_count')
    freight_certificate_ids = fields.One2many('freight.certificate', 'task_id', string='Freight Certificate')

    form6_count = fields.Integer(string='Form6', compute='_compute_form6')
    form9_count = fields.Integer(string='Form9', compute='_compute_form9')
    form6_ids = fields.One2many('movement.document', 'task_id', string='Form6')
    form9_ids = fields.One2many('form.document', 'task_id', string='Form9')
    form6 = fields.Binary(string="Form 6")
    form6_filename = fields.Char(string="Form 6 Filename")

    form9 = fields.Binary(string="Form 9")
    form9_filename = fields.Char(string="Form 9 Filename")

    def _compute_sale_order_count(self):
        for task in self:
            task.sale_order_count = len(task.sale_order_ids)

    # def _compute_purchase_order_count(self):
    #     for task in self:
    #         task.purchase_order_count = len(task.purchase_order_ids)


    @api.depends('purchase_order_ids')
    def _compute_purchase_order_count(self):
        for task in self:
            task.purchase_order_count = len(task.purchase_order_ids)

    def _compute_certificate_origin_count(self):
        for task in self:
            task.certificate_origin_count = len(task.certificate_origin_ids)

    def _compute_certificate_analysis_count(self):
        for task in self:
            task.certificate_analysis_count = len(task.certificate_analysis_ids)

    def _compute_packing_list_count(self):
        for task in self:
            task.packing_list_count = len(task.packing_list_ids)

    def _compute_freight_certificate_count(self):
        for task in self:
            task.freight_certificate_count = len(task.freight_certificate_ids)

    def _compute_form6(self):
        for task in self:
            task.form6_count = len(task.form6_ids)

    def _compute_form9(self):
        for task in self:
            task.form9_count = len(task.form9_ids)

    def action_view_sale_orders(self):
        return {
            'name': 'Sale Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('task_id', '=', self.id)],
            'context': {'default_task_id': self.id},
            'target': 'current',
        }



    def action_view_purchase_orders(self):
        return {
            'name': 'Purchase Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('task_id', '=', self.id)],
            'context': {'default_task_id': self.id},
        }

    # def action_view_purchase_orders(self):


    #     """Open related purchase orders."""
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Purchase Orders',
    #         'res_model': 'purchase.order',
    #         'view_mode': 'tree,form',
    #         'domain': [('task_id', '=', self.id)],
    #         'context': {'default_task_id': self.id},
    #         'target': 'current',
    #     }


    def action_view_certificate_origin(self):
        return {
            'name': 'Certificate Origin',
            'type': 'ir.actions.act_window',
            'res_model': 'certificate.origin',
            'view_mode': 'tree,form',
            'domain': [('task_id', '=', self.id)],
            'context': {'default_task_id': self.id},
            'target': 'current',


        }

    def action_view_certificate_analysis(self):
        return {
            'name': 'Certificate Origin',
            'type': 'ir.actions.act_window',
            'res_model': 'certificate.analysis',
            'view_mode': 'tree,form',
            'domain': [('task_id', '=', self.id)],
            'context': {'default_task_id': self.id},
            'target': 'current',
        }

    def action_view_packing_list(self):
        return {
            'name': 'Packing List',
            'type': 'ir.actions.act_window',
            'res_model': 'packing.list',
            'view_mode': 'tree,form',
            'domain': [('task_id', '=', self.id)],
            'context': {'default_task_id': self.id},
            'target': 'current',
        }

    def action_view_freight_certificate(self):
        return {
            'name': 'Freight Certificate',
            'type': 'ir.actions.act_window',
            'res_model': 'freight.certificate',
            'view_mode': 'tree,form',
            'domain': [('task_id', '=', self.id)],
            'context': {'default_task_id': self.id},
            'target': 'current',
        }

    def action_view_form6(self):
        return {
            'name': 'Form6',
            'type': 'ir.actions.act_window',
            'res_model': 'movement.document',
            'view_mode': 'tree,form',
            'domain': [('task_id', '=', self.id)],
            'context': {'default_task_id': self.id},
            'target': 'current',
        }

    def action_view_form9(self):
        return {
            'name': 'Form6',
            'type': 'ir.actions.act_window',
            'res_model': 'form.document',
            'view_mode': 'tree,form',
            'domain': [('task_id', '=', self.id)],
            'context': {'default_task_id': self.id},
            'target': 'current',
        }


