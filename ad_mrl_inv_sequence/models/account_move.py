from odoo import models,fields

class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_starting_sequence(self):
        """Called to determine invoice sequence format"""
        self.ensure_one()
        if self.move_type in ("out_invoice", "out_refund"):
            if self.company_id.name == "MRL Trading L.L.C":
                return "MRL/%(range_year)s/%(month)s/%(seq)s"
            elif self.company_id.name == "MRL Trading L.L.C - FZ":
                return "MRL-FZC/%(range_year)s/%(month)s/%(seq)s"
        return super()._get_starting_sequence()

    def _set_next_sequence(self):
        """Called on posting to generate the actual number"""
        for move in self:
            if move.move_type in ("out_invoice", "out_refund"):
                seq_date = move.invoice_date or move.date or fields.Date.today()
                if move.company_id.name == "MRL Trading L.L.C":
                    seq = self.env["ir.sequence"].next_by_code("account.move.mrl", sequence_date=seq_date)
                elif move.company_id.name == "MRL Trading L.L.C - FZ":
                    seq = self.env["ir.sequence"].next_by_code("account.move.mrl_fzc", sequence_date=seq_date)
                else:
                    seq = None
                if seq:
                    move.name = seq
            else:
                super(AccountMove, move)._set_next_sequence()
