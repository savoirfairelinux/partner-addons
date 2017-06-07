# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import _, api, models
from openerp.exceptions import UserError


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.multi
    def action_confirm(self):
        if self.partner_id.state != 'controlled':
            raise UserError(_(
                "Before validating this invoice, you have to validate "
                "the customer.")
            )

        super(StockPicking, self).action_confirm()

    @api.model
    def create(self, vals):
        if 'partner_id' in vals:
            partner = self.env['res.partner'].browse(vals['partner_id'])
            self._check_partner_sale_warn(partner)
        return super(StockPicking, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'partner_id' in vals:
            partner = self.env['res.partner'].browse(vals['partner_id'])
            self._check_partner_sale_warn(partner)
        return super(StockPicking, self).write(vals)

    def _check_partner_sale_warn(self, partner):
        if partner.sale_warn == 'warning':
            warn_msg = (
                self.env["ir.config_parameter"].get_param(
                    "partner.tracking.cod_warn_msg"))
            raise UserError(_(warn_msg))

        if partner.sale_warn == 'block':
            block_msg = (
                self.env["ir.config_parameter"].get_param(
                    "partner.tracking.cod_block_msg"))
            raise UserError(_(block_msg))
