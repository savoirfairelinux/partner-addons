# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Partner Tracking',
    'version': '10.0.1.0.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'LGPL-3',
    'category': 'Extra Rights',
    'depends': [
        'account',
        'mail',
        'sale',
    ],
    'data': [
        'data/ir_config_parameter.xml',
        'security/res_groups.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/sale_order.xml',
    ],
    'application': False,
    'installable': True,
}
