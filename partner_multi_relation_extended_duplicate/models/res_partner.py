# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    def _get_duplicates(self, indexed_name=None):
        res = []
        if not self._context.get('relation_duplication'):
            res = super(ResPartner, self)._get_duplicates(indexed_name)
        return res
