# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import status
import erpnext.controllers.status_updater
__version__ = '0.0.1'


erpnext.controllers.status_updater.status_map["Sales Order"][1] = status.so_to_deliver_and_bill
erpnext.controllers.status_updater.status_map["Sales Order"].insert(4, status.so_dropship)
erpnext.controllers.status_updater.status_map["Sales Order"].insert(1, status.so_backorder)

erpnext.controllers.status_updater.status_map["Purchase Order"][1] = status.po_to_receive_and_bill
erpnext.controllers.status_updater.status_map["Purchase Order"][3] = status.po_to_receive
erpnext.controllers.status_updater.status_map["Purchase Order"].insert(4, status.po_dropship)
