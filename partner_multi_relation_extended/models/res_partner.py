# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    relation_count_str = fields.Char(
        string='Relations',
        compute='_compute_relation_count_str')

    @api.depends('relation_count')
    def _compute_relation_count_str(self):
        for rec in self:
            rec.relation_count_str = str(rec.relation_count)

    @api.onchange('parent_id')
    def onchange_parent_id(self):
        res = super(ResPartner, self).onchange_parent_id()
        if self.parent_id:
            work_relation_type = self.env['res.partner.relation.type'].search([
                ('is_work_relation', '=', True),
            ])
            if not work_relation_type:
                res['warning'] = {
                    'title': _('Warning'),
                    'message': _('You cannot set a parent entity, as there is '
                                 'not any partner relation type flagged as '
                                 '"Work Relation".')
                }
                self.parent_id = False
        return res

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        if res.parent_id:
            work_relation_type = self.env['res.partner.relation.type'].search([
                ('is_work_relation', '=', True),
            ])
            self.env['res.partner.relation'].create({
                'left_partner_id': res.id,
                'right_partner_id': res.parent_id.id,
                'type_id': work_relation_type.id,
                'date_start': fields.Date.today(),
            })
        return res
