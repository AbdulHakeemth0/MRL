# -*- coding: utf-8 -*-
from shutil import copytree
from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    loading_ids = fields.Many2one('port.loading',string='Port Loading', copy=True)
    dis_ids = fields.Many2one('port.discharge',string='Port of Discharge', copy=True)
    time_ids = fields.Many2one('loading.time',string='Loading Time', copy=True)
    # des_ids = fields.Many2one('final.destination',string='Final Destination', copy=True)
    final_ids = fields.Many2one('final.destination',string='Final Destination', copy=True)
    mode_ids = fields.Many2one('mode.payment', string='Mode of Payment', copy=True)

