# Copyright (c) 2022, Jordan and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


def create_events():
    if frappe.flags.test_events_created:
        return

    frappe.set_user("Administrator")
    doc = frappe.get_doc({
        "doctype": "Article",
        "article_name":"_Test Article 1",
        "blurb": "article 1",
        "status": "Issued"
    }).insert()

    doc = frappe.get_doc({
        "doctype": "Article",
        "article_name":"_Test Article 2",
        "blurb": "article 2",
        "status": "Issued"
    	}).insert()

    frappe.flags.test_events_created = True


class TestArticle(FrappeTestCase):
	def setUp(self):
		create_events()

	def tearDown(self):
		frappe.set_user("Administrator")

	def test_not_allowed_public(self):
		frappe.set_user("test1@example.com")
		doc = frappe.get_doc("Article", frappe.db.get_value("Article",
    		{"article_name":"_Test Article 1"}))
		self.assertFalse(frappe.has_permission("Article", doc=doc))

	def test_not_allowed_private(self):
		frappe.set_user("test1@example.com")
		doc = frappe.get_doc("Article", frappe.db.get_value("Article",
    		{"article_name":"_Test Article 2"}))
		self.assertFalse(frappe.has_permission("Article", doc=doc))

