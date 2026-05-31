from odoo import fields, models


class FormDocument(models.Model):
    _name = 'form.document'

    task_id = fields.Many2one('project.task', string="Task")

    note = fields.Char(string='Notes')
    abbreviations = fields.Html(string='List Of Abbreviations Used')

    document_ids = fields.One2many('form.document.list', 'list_ids')


class FormDocumentList(models.Model):
    _name ='form.document.list'

    list_ids = fields.Many2one('form.document')
    sl_no = fields.Integer('Sl No')
    description = fields.Char()
    details = fields.Char()