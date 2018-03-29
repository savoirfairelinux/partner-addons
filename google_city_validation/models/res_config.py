# -*- coding: utf-8 -*-
# © 2018 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class CRMSettings(models.TransientModel):

    _name = 'sale.config.settings'
    _inherit = ['sale.config.settings']

    city_validation_policy = fields.Selection(
        [('soft', 'Soft'), ('strict', 'Strict')],
        help='Soft only warn the user / Strict delete the value of the city',
    )

    @api.model
    def get_default_policy(self, fields):
        policy = self.env['ir.config_parameter'].sudo().get_param(
            'google_city_validation.policy')
        return {'city_validation_policy': policy}

    @api.multi
    def set_policy(self):
        for rec in self:
            self.env['ir.config_parameter'].set_param(
                'google_city_validation.policy',
                rec.city_validation_policy or ''
            )
