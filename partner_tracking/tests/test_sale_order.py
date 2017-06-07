# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests import SavepointCase
from openerp.exceptions import UserError


class TestSaleOrder(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleOrder, cls).setUpClass()

        cls.partner = cls.env['res.partner'].create({
            'name': 'My Company',
            'is_company': True,
        })
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
        })

    def test_01_validate_sale_order_partner_controlled(self):
        self.partner.write({'state': 'controlled'})
        self.sale_order.action_confirm()

    def test_02_validate_sale_order_partner_not_controlled(self):
        self.partner.write({'state': 'pending'})
        with self.assertRaises(UserError):
            self.sale_order.action_confirm()

    def test_03_write_on_sale_order_partner_blocked(self):
        partner_1 = self.env['res.partner'].create({
            'name': 'My Partner 1',
            'sale_warn': 'block',
        })
        with self.assertRaises(UserError):
            self.sale_order.write({'partner_id': partner_1.id})

        block_msg = (
            self.env["ir.config_parameter"].get_param(
                "partner.tracking.cod_block_msg"))
        self.assertTrue(block_msg)

    def test_04_create_sale_order_partner_warning(self):
        partner_1 = self.env['res.partner'].create({
            'name': 'My Partner 1',
            'sale_warn': 'warning',
        })
        with self.assertRaises(UserError):
            self.sale_order = self.env['sale.order'].create({
                'partner_id': partner_1.id,
            })

        warn_msg = (
            self.env["ir.config_parameter"].get_param(
                "partner.tracking.cod_warn_msg"))
        self.assertTrue(warn_msg)
