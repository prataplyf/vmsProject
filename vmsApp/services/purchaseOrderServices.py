# import modules
from ..models import PurchaseOrder
from ..serializers import PurchaseOrderSerializer
from ..repository.purchaseOrderRepo import PurchasedOrderRepository


class PurhaseOrderService:
    """
    Service class for handling purchase order data operations.

    This class provides methods for interacting with purchase order data, likely
    using a repository (`PurchasedOrderRepository`) for persistence logic (e.g., database access).
    """
    def __init__(self):
        """
        Initializes the PurchaseOrderService instance.

        This constructor establishes a connection with the `PurchasedOrderRepository` instance.
        """
        self.po_repo = PurchasedOrderRepository()

    def get_all_orders(self):
        """
        Retrieves all purchase orders.

        This function retrieves a list of all purchase orders from the repository.
        Output:
            list or None:
                On success, it returns a list of purchase orders in a format suitable for serialization
                (likely a dictionary representation).
                On failure, it returns None. Consider returning a more informative value or raising an exception.
        """
        try:        
            po_list = self.po_repo.get_all_purchased_orders() #.order_by('-created_at')
            serializer = PurchaseOrderSerializer(po_list, many=True)
            return serializer.data
        except Exception as e:
            return None
    
    def create_order(self, data):
        """
        Creates a new purchase order.

        This function creates a new purchase order based on the provided data.

        Args:
            data (dict): A dictionary containing purchase order details.

        Output:
            dict or None:
                On success (if the purchase order is created), it returns a dictionary representing
                the newly created purchase order data.
                On failure (including cases where data validation fails), it returns None.
                Consider returning a more informative value or raising an exception.
        """
        try:
            serializer = PurchaseOrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            else:
                return None
        except Exception as e:
            return None
    
    def get_purchase_order_detail(self, order_id):
        """
        Retrieves a specific purchase order.

        This function retrieves a purchase order with the provided `order_id` from the repository.

        Args:
            order_id (int): The ID of the purchase order to retrieve.

        Output:
            dict or None:
                On success (if the purchase order is found), it returns a dictionary representing
                the retrieved purchase order details.
                On failure (including cases where the purchase order is not found), it returns None.
                Consider returning a more informative value (e.g., a specific exception).
        """
        try:
            po = self.po_repo.get_purchased_order_by_id(order_id)
            if not po:
                return f"Purchased order for id {order_id} not found"
            serializer = PurchaseOrderSerializer(po)
            return serializer.data
        except Exception as e:
            return None
    
    def update_order(self, order_id, data):
        """
        Updates a purchase order.

        This function updates a purchase order with the provided `order_id` based on the given data.

        Args:
            order_id (int): The ID of the purchase order to update.
            data (dict): A dictionary containing update information for the purchase order.

        Output:
            dict or None:
                On success (if the purchase order is found and updated), it returns a dictionary
                representing the updated purchase order details.
                On failure (including cases where the purchase order is not found or update fails),
                it returns None. Consider returning a more informative value (e.g., validation errors).
        """
        try:
            po = self.po_repo.get_purchased_order_by_id(order_id)
            if not po:
                return f"Purchased order for id {order_id} not found"
            serializer = PurchaseOrderSerializer(po, data=data)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            else:
                return None
        except Exception as e:
            return None
        
    def delete_order(self, order_id):
        """
        Deletes a purchase order.

        This function deletes a purchase order with the provided `order_id` from the repository.

        Args:
            order_id (int): The ID of the purchase order to delete.

        Output:
            boolean or None:
                On success (if the purchase order is found and deleted), it returns True.
                On failure (including cases where the purchase order is not found), it returns None.
                Consider returning a more informative value (e.g., a specific exception).
        """
        try:
            delete_po = self.po_repo.delete_purchased_order(order_id)
            if not delete_po:
                return f"Purchased order for id {order_id} not found"            
            return delete_po
        except Exception as e:
            return None
