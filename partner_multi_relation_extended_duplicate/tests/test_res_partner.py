# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestResPartner(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestResPartner, cls).setUpClass()
        cls.partner_model = cls.env['res.partner']
        cls.type_model = cls.env['res.partner.relation.type']
        cls.wizard_model = cls.env['res.partner.parent.modification']

        cls.companies = [cls.partner_model.create({
            'name': 'Test Company %s' % i,
            'is_company': True,
        }) for i in range(2)]

        cls.individual = cls.partner_model.create({
            'name': 'Test individual',
            'is_company': False,
            'email': 'test%s@email',
            'parent_id': cls.companies[0].id,
        })

        cls.work_relation_type = cls.type_model.create({
            'name': 'works for',
            'name_inverse': 'has employee',
            'is_work_relation': True,
        })

        cls.relation_type_same = cls.env.ref(
            'partner_multi_relation_extended.rel_type_same')

    def test_01_partner_change_entity(self):
        """
        Test standard parent modification, which should not generate any
        duplicate
        """
        new_company = self.companies[1]
        wizard = self.wizard_model.with_context({
            'active_id': self.individual.id,
            'active_model': 'res.partner',
        }).create({
            'new_company_id': new_company.id,
        })
        wizard.validate()
        new_contact = self.partner_model.search([
            ('name', '=', self.individual.name),
            ('parent_id', '=', new_company.id),
        ])
        self.assertFalse(new_contact.duplicate_ids)

    def test_02_real_duplicate(self):
        """
        Test similar partner not from parent modification
        """
        similar = self.partner_model.create({
            'name': 'Test individual',
            'is_company': False,
        })
        self.assertEqual(len(similar.duplicate_ids), 1)
