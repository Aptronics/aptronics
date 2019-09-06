# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__version__ = '0.0.1'

try:
    from aptronics import overrides
    from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
    SalesInvoice._original_get_gl_entries = SalesInvoice.get_gl_entries
    SalesInvoice.get_gl_entries = overrides.get_gl_entries
    print('patched Sales Invoice')
except Exception as e:
    print('failed to patch Sales Invoice' + str(e))
