from odoo import models, fields

class TransactionLine(models.Model):
    _name = 'transaction.line'
    _description = 'Transaction Line'

    transaction_id = fields.Many2one('library.transaction', string="Transaction")
    book_id = fields.Many2one('book.records', string="Book", required=True)
    customer_id = fields.Many2one('user.records',string="User", required=True)
    quantity = fields.Integer(string="Quantity", default=1)
    available = fields.Integer(string="Available Copies", related="book_id.available_copies", readonly=True)
