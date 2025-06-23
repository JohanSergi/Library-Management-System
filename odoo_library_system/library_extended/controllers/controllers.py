# -*- coding: utf-8 -*-
# from odoo import http


# class LibraryExtended(http.Controller):
#     @http.route('/library_extended/library_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/library_extended/library_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('library_extended.listing', {
#             'root': '/library_extended/library_extended',
#             'objects': http.request.env['library_extended.library_extended'].search([]),
#         })

#     @http.route('/library_extended/library_extended/objects/<model("library_extended.library_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('library_extended.object', {
#             'object': obj
#         })
