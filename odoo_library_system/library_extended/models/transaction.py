from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError

class LibraryTransaction(models.Model):
    _name = 'library.transaction'
    _description = 'Library Transaction'

    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
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
    fine_amount = fields.Float(string="Fine Amount", compute="_compute_fine", store=True)

    @api.depends('date_returned', 'due_date', 'state')
    def _compute_fine(self):
        fine_per_day = 10
        for record in self:
            if record.date_returned and record.due_date and record.state == 'returned':
                delay_days = (record.date_returned - record.due_date).days
                if delay_days > 0:
                    record.fine_amount = fine_per_day * delay_days
                else:
                    record.fine_amount = 0.0
            else:
                record.fine_amount = 0.0

    @api.depends('transaction_line_ids.quantity')
    def _compute_total_quantity(self):
        for record in self:
            record.total_quantity = sum(line.quantity for line in record.transaction_line_ids)

    def action_take_book(self):
        stock_location = self.env.ref('stock.stock_location_stock')
        customer_location = self.env.ref('stock.stock_location_customers')

        for transaction in self:
            if transaction.state != 'draft':
                raise ValidationError("Books can only be taken in Draft state.")
            if transaction.total_quantity > 5:
                raise ValidationError("Exceeds Limit..!")

            for line in transaction.transaction_line_ids:
                if line.book_id.qty_available < line.quantity:
                    raise ValidationError(
                        f"Not enough copies for '{line.book_id.name}'. Available: {line.book_id.qty_available}"
                    )
                if transaction.customer_id.books_due > 4:
                    raise ValidationError(
                        f"Exceeds the limit. Already Taken: {transaction.customer_id.books_due} books."
                    )
                # Create stock move
                self.env['stock.move'].create({
                    'name': f'Library Book Issue: {line.book_id.name}',
                    'product_id': line.book_id.id,
                    'product_uom': line.book_id.uom_id.id,
                    'product_uom_qty': line.quantity,
                    'location_id': stock_location.id,
                    'location_dest_id': customer_location.id,
                })._action_done()
            transaction.customer_id.books_due += transaction.total_quantity
            transaction.due_date = transaction.date_taken + timedelta(weeks=2)
            transaction.state = 'taken'

    def action_return_book(self):
        stock_location = self.env.ref('stock.stock_location_stock')
        customer_location = self.env.ref('stock.stock_location_customers')

        for transaction in self:
            if transaction.state != 'taken':
                raise ValidationError("Books can only be returned after they've been taken.")

            for line in transaction.transaction_line_ids:
                self.env['stock.move'].create({
                    'name': f'Library Book Return: {line.book_id.name}',
                    'product_id': line.book_id.id,
                    'product_uom': line.book_id.uom_id.id,
                    'product_uom_qty': line.quantity,
                    'location_id': customer_location.id,
                    'location_dest_id': stock_location.id,
                })._action_done()
            transaction.customer_id.books_due -= transaction.total_quantity
            transaction.date_returned = fields.Date.context_today(self)
            transaction.state = 'returned'

