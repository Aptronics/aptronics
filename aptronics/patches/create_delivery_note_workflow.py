import frappe

def execute():
    if frappe.get_value('Workflow', 'Delivery Note Goods in Transit', 'name'):
        print('Delivery Note Goods in Transit Workflow Already Installed')
        return
    wf = frappe.new_doc("Workflow")
    wf.document_type = 'Delivery Note'
    wf.workflow_name = 'Delivery Note Goods in Transit'
    wf.workflow_state_field = 'workflow_state'
    wf.send_email_alert = 0
    wf.is_active = 1
    wf.append('states', {"state": "Draft",
        "doc_status": 0,
        "allow_edit": "All"})
    wf.append('states', {"state": "Goods in Transit",
        "doc_status": 0,
        "allow_edit": "All"})
    wf.append('states', {"state": "Submitted",
        "doc_status": 1,
        "allow_edit": "All"})
    wf.append('states',
        {"state": "Cancelled",
        "doc_status": 2,
        "allow_edit": "All"})
    ####
    wf.append("transitions", {"state": "Draft",
        "action": "Save",
        "next_state": "Draft",
        "allowed": "All"})
    wf.append("transitions", {"state": "Draft",
        "action": "Ship Goods",
        "next_state": "Draft",
        "allowed": "All"})
    wf.append("transitions", {"state": "Draft",
        "action": "Customer Pickup",
        "next_state": "Submitted",
        "allowed": "All"})
    wf.append("transitions", {"state": "Goods in Transit",
        "action": "Mark Shipment Delivered",
        "next_state": "Submitted",
        "allowed": "All"})
    wf.append("transitions", {"state": "Goods in Transit",
        "action": "Return Goods in Transit",
        "next_state": "Draft",
        "allowed": "All"})
    wf.append("transitions", {"state": "Goods in Transit",
        "action": "Deliver and Create Invoice",
        "next_state": "Submitted",
        "allowed": "All"})
    wf.append("transitions", {"state": "Submitted",
        "action": "Cancel",
        "next_state": "Cancelled",
        "allowed": "All"})
    wf.save()
