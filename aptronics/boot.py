
from . import overrides
import erpnext.accounts.doctype.sales_invoice as si

def boot_session(bootinfo):
    from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
    SalesInvoice.get_gl_entries = overrides.get_gl_entries
    return bootinfo
