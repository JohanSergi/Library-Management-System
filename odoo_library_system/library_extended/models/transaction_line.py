from odoo import models, fields

class TransactionLine(models.Model):
    _name = 'transaction.line'
    _description = 'Transaction Line'

    transaction_id = fields.Many2one('library.transaction', string="Transaction")
    book_id = fields.Many2one('product.product', string="Book", required=True)
    quantity = fields.Integer(string="Quantity", default=1)
    available = fields.Float(string="Available Copies", related="book_id.qty_available", readonly=True)
