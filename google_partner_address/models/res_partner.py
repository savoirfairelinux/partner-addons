# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    @api.onchange('zip')
    def _onchange_zip(self):
        self.zip = self.zip.upper() if self.zip else ""

    copy_place = fields.Char(
        string='Full Address',
        readonly=True,
    )
