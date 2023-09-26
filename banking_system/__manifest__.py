# -*- coding: utf-8 -*-
{
    'name': "banking_system",

    'summary': "Here you can use banking system's deposit management system, "
               "like multiple banks handle, customers profile and its balance, "
               "transaction details and notification you can send also print "
               "transaction receipt.",

    'description': "Here you can use banking system's deposit management system, "
               "like multiple banks handle, customers profile and its balance, "
               "transaction details and notification you can send also print "
               "transaction receipt.",

    'author': "Iqbal Elham",
    'website': "https://iqbal-elham.onrender.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    'application': True,
    'sequence': -1001,

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/bank_view.xml',
        'views/banker_customer_view.xml',
        'views/banker_transactions.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
