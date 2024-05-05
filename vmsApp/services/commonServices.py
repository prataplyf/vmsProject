# import modules
from rest_framework import status
from django.utils import timezone
from ..models import PurchaseOrder
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ..serializers import PurchaseOrderSerializer
from ..repository.purchaseOrderRepo import PurchasedOrderRepository
from ..repository.vendorRepo import VendorRepository


    

class CommonService:
    """
    Service class for handling common purchase order operations.

    This class provides methods for interacting with purchase orders, potentially
    including tasks shared by multiple API views. It interacts with repositories
    for purchase orders and vendors.
    """

    def __init__(self):
        """
        Initializes the CommonService instance.

        This constructor establishes connections with the `PurchasedOrderRepository`
        and `VendorRepository` instances, likely handling persistence logic for
        purchase orders and vendors (e.g., database access).
        """
        self.po_repo = PurchasedOrderRepository()
        self.vendor_repo = VendorRepository()
    
    def get_acknowledged_purchase_orders(self, po_id):
        """
        Acknowledges a purchase order by its ID.

        This function handles acknowledging a purchase order with the provided `po_id`.
        It utilizes a try-except block to handle potential exceptions.

        On success (if the purchase order is acknowledged), it returns 1 (consider
        returning a more informative value or a success object).

        On failure (including cases where the purchase order is not found or already
        acknowledged), it raises an exception to be caught by the calling API view.

        **Note:** Consider improving the error handling by returning specific exceptions
        with informative messages instead of raising generic exceptions.
        """
        try:
            purchase_order = self.po_repo.get_purchased_order_by_id(po_id)
            if purchase_order.acknowledgment_date is not None:
                return Response({'message': 'Purchase order already acknowledged', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

             # Update acknowledgment date
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()

            # Trigger vendor performance recalculation
            purchase_order.vendor.calculate_performance_metrics()
            purchase_order.vendor.save()              
            return 1
        except Exception as e:
            raise None

    def completed_purchase_orders(self, po_id):
        """
        Marks a purchase order as completed.

        This function handles marking a purchase order with the provided `po_id` as completed.
        It utilizes a try-except block to handle potential exceptions.

        On success (if the purchase order is marked as completed), it returns 1 (consider
        returning a more informative value or a success object).

        On failure (including cases where the purchase order is not found or is already
        completed or cancelled), it raises an exception to be caught by the calling API view.
        """
        try:            
            purchase_order = self.po_repo.get_purchased_order_by_id(po_id)
            if purchase_order.status != 'pending':
                return Response({'message': 'Purchase order already completed or cancelled'}, status=status.HTTP_400_BAD_REQUEST)
            
            purchase_order.status = 'completed'
            purchase_order.save()

            
            # Trigger performance metric recalculation for the vendor
            purchase_order.vendor.calculate_performance_metrics()
            purchase_order.vendor.save_performance_history()
            return 1
        except Exception as e:
            raise None
    
    def update_quality_rating(self, po_id, data):
        """
        Updates the quality rating of a purchase order.

        This function handles updating the quality rating of a purchase order with the provided
        `po_id`. It expects the quality rating information in the request data (`data`).
        It utilizes a try-except block to handle potential exceptions.

        On success (if the quality rating is updated), it returns 1 (consider returning
        a more informative value or a success object).

        On failure (including cases where the purchase order is not found, the status is not
        'completed', or the update fails), it raises an exception to be caught by the calling
        API view.
        """
        try:
            purchase_order = self.po_repo.get_purchased_order_by_id(po_id)
            if purchase_order.status != 'completed':
                return Response({'message': 'Cannot update quality rating for non-completed PO'}, status=status.HTTP_400_BAD_REQUEST)

            # Update quality rating and potentially other fields
            purchase_order.quality_rating = data.get('quality_rating')
            purchase_order.save()

            # Trigger performance metric recalculation for the vendor
            purchase_order.vendor.calculate_performance_metrics()
            purchase_order.vendor.save_performance_history()
            return 1
        except Exception as e:
            raise None