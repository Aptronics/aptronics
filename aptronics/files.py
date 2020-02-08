import frappe

@frappe.whitelist()
def confirm_delete_of_submitted_doc(doc, method):
    linked_docstatus = frappe.get_value(
        doc.attached_to_doctype, doc.attached_to_name, 'docstatus'
    )
    if linked_docstatus == 1:
        frappe.permissions.check_admin_or_system_manager()
        # frappe.throw("This file is attached to a submitted document.")
