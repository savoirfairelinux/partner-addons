# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests import SavepointCase
from openerp.exceptions import UserError


class TestStockPicking(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestStockPicking, cls).setUpClass()

        cls.partner = cls.env['res.partner'].create({
            'name': 'My Company',
            'is_company': True,
        })
        cls.location = cls.env['stock.location'].create({
            'name': 'My Location',
        })
        cls.location_dest = cls.env['stock.location'].create({
            'name': 'My Location Dest',
        })
        cls.sequence = cls.env['ir.sequence'].create({
            'name': 'My Sequence',
        })
        cls.picking_type = cls.env['stock.picking.type'].create({
            'name': 'My Picking Type',
            'sequence_id': cls.sequence.id,
            'code': 'outgoing',
        })
        cls.stock_picking = cls.env['stock.picking'].create({
            'partner_id': cls.partner.id,
            'location_id': cls.location.id,
            'location_dest_id': cls.location_dest.id,
            'picking_type_id': cls.picking_type.id,
        })

    def test_01_validate_stock_picking_partner_controlled(self):
        self.partner.write({'state': 'controlled'})
        self.stock_picking.action_confirm()

    def test_02_validate_stock_picking_partner_not_controlled(self):
        self.partner.write({'state': 'pending'})
        with self.assertRaises(UserError):
            self.stock_picking.action_confirm()

    def test_03_write_on_stock_picking_partner_blocked(self):
        partner_1 = self.env['res.partner'].create({
            'name': 'My Partner 1',
            'sale_warn': 'block',
        })
        with self.assertRaises(UserError):
            self.stock_picking.write({'partner_id': partner_1.id})

        block_msg = (
            self.env["ir.config_parameter"].get_param(
                "partner.tracking.cod_block_msg"))
        self.assertTrue(block_msg)

    def test_04_create_stock_picking_partner_warning(self):
        partner_1 = self.env['res.partner'].create({
            'name': 'My Partner 1',
            'sale_warn': 'warning',
        })
        with self.assertRaises(UserError):
            self.stock_picking = self.env['stock.picking'].create({
                'partner_id': partner_1.id,
                'location_id': self.location.id,
                'location_dest_id': self.location_dest.id,
                'picking_type_id': self.picking_type.id,
            })

        warn_msg = (
            self.env["ir.config_parameter"].get_param(
                "partner.tracking.cod_warn_msg"))
        self.assertTrue(warn_msg)
