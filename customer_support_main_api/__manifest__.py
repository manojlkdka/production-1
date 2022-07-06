# -*- coding: utf-8 -*-
{
    'name': "Customer Support Main Rest Api (Json)",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        1) Open odoo.conf
        2) Add 'dbfilter = dbname'.
        3) Restart odoo service.
    """,

    'author': "Manoj Khadka",
    'website': "-",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    'data': [
        'security/ir.model.access.csv',
        "data/ir_config_param.xml", 
        'views/views.xml',
        'views/access_token_config.xml'
    ],
    'demo': [
    ],
}
