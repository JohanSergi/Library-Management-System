from odoo import models, fields,api
from datetime import timedelta
from odoo.exceptions import ValidationError

class LibraryTransaction(models.Model):
    _name = 'library.transaction'
    _description = 'Library Transaction'

    customer_id = fields.Many2one('user.records', string="Customer", required=True)
    date_taken = fields.Date(string="Date Taken", default=fields.Date.context_today)
    date_returned = fields.Date(string="Date Returned")
    due_date = fields.Date(string="Due Date")
    transaction_line_ids = fields.One2many('transaction.line', 'transaction_id', string="Books Borrowed")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('taken', 'Taken'),
        ('returned', 'Returned')
    ], string='Status', default='draft')
    total_quantity = fields.Integer(string="Total Quantity", compute="_compute_total_quantity", store=True)

    @api.depends('transaction_line_ids.quantity')
    def _compute_total_quantity(self):
        for record in self:
            record.total_quantity = sum(line.quantity for line in record.transaction_line_ids)

    def action_take_book(self):
        for transaction in self:
            if transaction.state != 'draft':
                raise ValidationError("Books can only be taken in Draft state.")
            if transaction.total_quantity > 5:
                raise ValidationError("Exceeds Limit..!")
            for line in transaction.transaction_line_ids:
                if line.book_id.available_copies < line.quantity:
                    raise ValidationError(
                        f"Not enough copies for '{line.book_id.title}'. Available: {line.book_id.available_copies}"
                    )
                if transaction.customer_id.books_taken > 4:
                    raise ValidationError(
                        f"Exceeds the limit. Already Taken: {transaction.customer_id.books_taken} books."
                    )
                transaction.customer_id.books_taken += line.quantity
                line.book_id.available_copies -= line.quantity
                transaction.due_date = transaction.date_taken + timedelta(weeks=2)
            transaction.state = 'taken'

    def action_return_book(self):
        for transaction in self:
            if transaction.state != 'taken':
                raise ValidationError("Books can only be returned after they've been taken.")
            for line in transaction.transaction_line_ids:
                transaction.customer_id.books_taken -= line.quantity
                line.book_id.available_copies += line.quantity
            transaction.state = 'returned'
            transaction.date_returned=fields.Date.context_today(self)
