# -*- coding: utf-8 -*-
# © 2018 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Google City Validation',
    'version': '10.0.1.0.1',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'LGPL-3',
    'category': 'Base',
    'summary': 'City validation',
    'depends': [
        'base',
        'web',
        'crm',
    ],
    'data': [
        'data/ir_config_parameter.xml',
        'views/assets.xml',
        'views/res_config_views.xml',
    ],
    'installable': True,
}
