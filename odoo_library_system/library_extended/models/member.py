from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_library_member = fields.Boolean(string="Library Member", default=False)
    # member = fields.Char(string="Member ID")
    books_due = fields.Integer(string="Books Due", default=0)
    transaction_count = fields.Integer(string="Transactions", compute='_compute_transaction_count')

    def _compute_transaction_count(self):
        for partner in self:
            partner.transaction_count = self.env['library.transaction'].search_count([
                ('customer_id', '=', partner.id)
            ])

    def open_member_transactions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Member Transactions',
            'view_mode': 'tree,form',
            'res_model': 'library.transaction',
            'domain': [('customer_id', '=', self.id)],
            'context': {'default_customer_id': self.id},
        }

