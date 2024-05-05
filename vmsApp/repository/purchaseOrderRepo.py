# import modules
from ..models import PurchaseOrder

class PurchasedOrderRepository:
    def __init__(self):
        self.purchased_orders = []
    
    
    def get_all_purchased_orders(self):
        return PurchaseOrder.objects.all()
    
    def get_purchased_order_by_id(self, po_id):
        return PurchaseOrder.objects.get(pk=po_id)
    
    def delete_purchased_order(self, po_id):
        po = self.get_purchased_order_by_id(po_id)
        if not po:
            return None
        po.delete()
        return po