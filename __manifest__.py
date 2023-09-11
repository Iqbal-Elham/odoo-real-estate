# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': """
        The Real estate""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Iqbal Elham",
    'website': "https://iqbal-elham.onrender.com",
    'application': True,
    'sequence': -1000,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
