from odoo import models, fields, api
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            company_id = vals.get('company_id') or self.env.company.id
            company = self.env['res.company'].browse(company_id)

            if company.name == 'MRL Trading L.L.C':
                seq_code = 'sale.order.mrl_llc'
            else:
                seq_code = 'sale.order.mrl_fzc'

            vals['name'] = self.env['ir.sequence'].next_by_code(seq_code) or 'New'

        return super(SaleOrder, self).create(vals)









class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') in ['New', False]:
            company_id = vals.get('company_id') or self.env.company.id
            company = self.env['res.company'].browse(company_id)

            if company.name == 'MRL Trading L.L.C':
                seq_code = 'purchase.order.mrl_llc'
            else:
                seq_code = 'purchase.order.mrl_fzc'


            vals['name'] = self.env['ir.sequence'].next_by_code(seq_code) or 'New'

        return super(PurchaseOrder, self).create(vals)

# class AccountMove(models.Model):
#     _inherit = 'account.move'
#
#     @api.model
#     def create(self, vals):
#         # Only generate sequence if name is "New"
#         if vals.get('name', 'New') in ['New', False]:
#             company_id = vals.get('company_id') or self.env.company.id
#             company = self.env['res.company'].browse(company_id)
#
#             # Select sequence by company name
#             if company.name == 'MRL-LLC':
#                 seq_code = 'account.move.mrl_llc'
#             else:
#                 seq_code = 'account.move.mrl_fzc'
#
#             # Generate sequence properly
#             vals['name'] = self.env['ir.sequence'].next_by_code(seq_code) or '/'
#
#         return super(AccountMove, self).create(vals)
#
#

