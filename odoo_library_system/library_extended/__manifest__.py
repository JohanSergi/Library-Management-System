# -*- coding: utf-8 -*-
{
    'name': 'Library Management System',
    'version': '1.0',
    'depends': ['base', 'product', 'sale'],
    'category': 'Library',
    'summary': 'Manage library books and members using Odoo standard models',
    'description': 'Library module using product.template for books and res.partner for members.',
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/library_book_views.xml',
        'views/library_member_views.xml',
        'reports/library_transaction_report.xml',
        'reports/report_transaction.xml',
        'views/library_transaction_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
