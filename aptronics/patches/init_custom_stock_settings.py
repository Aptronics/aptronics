import frappe

def execute():
    print("Initializing Stock Settings Custom Fields")
    doc = frappe.get_doc("Stock Settings")
    if not doc.get("cogs_on_invoice"):
        doc.cogs_on_invoice = 1
    doc.save()
