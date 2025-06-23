from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_library_book = fields.Boolean(string="Is a Library Book", default=False)
    author = fields.Char()
    language = fields.Char()
    genre = fields.Selection([
        ('novel', 'Novel'),
        ('fantasy', 'Fantasy'),
        ('other', 'Other')
    ], string="Genre")
