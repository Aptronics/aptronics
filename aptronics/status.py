
# override to ["Sales Order"][3]
so_backorder = [u'Back Ordered', u'eval: self.total_backordered_qty > 0 and self.status != "Closed" and self.docstatus == 1']

# override to ["Sales Order"][1]
so_to_deliver_and_bill = [u'To Deliver and Bill', u"eval:self.per_delivered < 100 and self.per_billed < 100 and self.docstatus == 1 and self.order_type in ['Sales', 'Shopping Cart'] and self.total_backordered_qty == 0"]

# insert: ["Sales Order"].insert(4, dropship)
so_dropship = [u'Drop Shipped', u'eval: self.delivery_status == \'Drop Shipped\' and self.docstatus == 1 and self.total_backordered_qty == 0']

# insert: ["Purchase Order"].insert(4, dropship)
po_dropship = [u'Drop Shipped', u'eval:self.per_drop_shipped == 100 and self.docstatus == 1 and self.customer']

po_to_receive_and_bill = [u'To Receive and Bill', u'eval:self.per_drop_shipped < 100 and self.per_received < 100 and self.per_billed < 100 and self.docstatus == 1 and not self.customer']

po_to_receive = [u'To Receive', u'eval:self.per_drop_shipped < 100 and self.per_received < 100 and self.per_billed == 100 and self.docstatus == 1 and not self.customer']
