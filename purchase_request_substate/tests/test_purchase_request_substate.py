# Copyright 2021 Ecosoft (<http://ecosoft.co.th>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPurchaseRequestSubstate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Prepare PR
        cls.purchase_request_obj = cls.env["purchase.request"]
        cls.purchase_request_line_obj = cls.env["purchase.request.line"]
        cls.wiz = cls.env["purchase.request.line.make.purchase.order"]
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
            }
        )
        vals = {
            "picking_type_id": cls.env.ref("stock.picking_type_in").id,
            "requested_by": SUPERUSER_ID,
        }
        cls.pr_test = cls.purchase_request_obj.create(vals)
        vals = {
            "request_id": cls.pr_test.id,
            "product_id": cls.product.id,
            "product_uom_id": cls.env.ref("uom.product_uom_unit").id,
            "product_qty": 5.0,
        }
        cls.purchase_request_line_obj.create(vals)

        # Prepare states: the test brings its own substates instead of relying
        # on the demo data of this module. Substates already defined for this
        # type are archived first, so that the default substate is
        # deterministic whether or not demo data is loaded
        # (_get_default_substate_id searches with order="sequence", limit=1,
        # and search() leaves out archived records).
        substate_obj = cls.env["base.substate"]
        substate_type = cls.env.ref(
            "purchase_request_substate.base_substate_type_purchase_request"
        )
        target_to_approve = cls.env.ref(
            "purchase_request_substate.target_state_value_to_approve"
        )
        substate_obj.search(
            [
                (
                    "target_state_value_id.base_substate_type_id",
                    "=",
                    substate_type.id,
                )
            ]
        ).active = False
        cls.substate_to_verify = substate_obj.create(
            {
                "name": "To Verify",
                "sequence": 1,
                "target_state_value_id": target_to_approve.id,
            }
        )
        cls.substate_checked = substate_obj.create(
            {
                "name": "Checked",
                "sequence": 2,
                "target_state_value_id": target_to_approve.id,
            }
        )
        cls.substate_verified = substate_obj.create(
            {
                "name": "Verified",
                "sequence": 3,
                "target_state_value_id": target_to_approve.id,
                "mail_template_id": cls.env.ref(
                    "purchase_request_substate."
                    "mail_template_data_purchase_request_substate_verified"
                ).id,
            }
        )

    def test_purchase_request_order_substate(self):
        self.assertTrue(self.pr_test.state == "draft")
        self.assertTrue(not self.pr_test.substate_id)

        # Block substate not corresponding to draft state
        with self.assertRaises(ValidationError):
            self.pr_test.substate_id = self.substate_to_verify
        # Test that validation of purchase_request order change substate_id
        self.pr_test.button_to_approve()
        self.assertTrue(self.pr_test.state == "to_approve")
        self.assertTrue(self.pr_test.substate_id == self.substate_to_verify)

        # Test that substate_id is set to false if
        # there is not substate corresponding to state
        self.pr_test.button_approved()
        self.assertTrue(self.pr_test.state == "approved")
        self.assertTrue(not self.pr_test.substate_id)
