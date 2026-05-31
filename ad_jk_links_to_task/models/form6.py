from odoo import api, fields, models


class MovementDocument(models.Model):
    _name = 'movement.document'

    task_id = fields.Many2one('project.task', string="Task")

    note = fields.Char(string='Notes')
    abbreviations = fields.Html(string='List Of Abbreviations Used')

    document_ids = fields.One2many('movement.document.list', 'list_ids')


class MovementDocumentList(models.Model):
    _name ='movement.document.list'

    list_ids = fields.Many2one('movement.document')
    sl_no = fields.Integer('Sl No')
    description = fields.Char()
    details = fields.Char()