from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ..models import PurchaseOrder
from django.utils import timezone
from ..services.purchaseOrderServices import PurhaseOrderService

class POBaseModel(APIView):
    """
    Base class for API views related to purchase orders. API views can access
    the `po_service` instance and utilize its methods for handling purchase order data.
    """
    def __init__(self):
        """
        Initializes the POBaseModel instance.
        This constructor establishes a connection with the `PurchaseOrderService` instance.
        """
        self.po_service = PurhaseOrderService()


class PurchaseOrderAPI(POBaseModel):
    """
    API endpoint for retrieving a list of all purchase orders.
    This class handles GET requests to retrieve a list of all purchase orders.
    """
  
    def get(self, request):
        """
        Retrieves a list of all purchase orders.
        
        **GET http://127.0.0.1:8000/api/purchase_orders/ **
        This function handles GET requests to retrieve all purchase orders.
        """
        try:
            po_list = self.po_service.get_all_orders()
            return Response({'message': 'Successfully fetched purchased order records', 'status': 200, "data": {"po": po_list}}, status=status.HTTP_200_OK)
        except Exception as e:  # Catch any exceptions during retrieval
            return Response({'message': f'An error occurred: {str(e)}', 'status': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def post(self, request):
        """
        Creates a new purchase order.
        **POST http://127.0.0.1:8000/api/purchase_orders/ **
        
        **POST /purchase_orders/**
        This function handles POST requests to create a new purchase order. It expects the
        purchase order details in the request body.
        """
        try:
            po_status = self.po_service.create_order(request.data)
            if not po_status:
                raise ValueError("failed to create purchase order")
            return Response({
                'message': 'Purchase order created successfully',
                'data': po_status,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Validation errors occurred', 'errors': f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


            


class PurchasedOrderViewAPI(POBaseModel):
    """
    API endpoint for retrieving, updating, and deleting a specific purchase order.
    This class handles GET, PUT, and DELETE requests for a purchase order identified by its ID.
    It inherits from `POBaseModel` to access the `po_service` instance.
    """

    def get(self, request, po_id):
        """
        Retrieves a specific purchase order.

        **GET http://127.0.0.1:8000/api/purchase_orders/{po_id}/ **
        """
        try:
            po_details = self.po_service.get_purchase_order_detail(po_id)
            if not po_details:
                raise NotFound('Purchased Order with ID {} not found.'.format(po_id))
            
            return Response({'message': 'Successfully fetched order record', 'status': 200, "data": {"po": po_details}})
        except Exception as e:  # Catch any exceptions during retrieval
            return Response({'message': f'An error occurred: {str(e)}', 'status': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def put(self, request, po_id):
        """
        Updates a purchase order.

        **PUT http://127.0.0.1:8000/api/purchase_orders/{po_id}/ **

        This function handles PUT requests to update a purchase order with the provided `po_id`.
        It expects the update details in the request body.
        """
        try:
            update_po = self.po_service.update_order(po_id, request.data)
            if not update_po:
                raise NotFound('Purchased Order with ID {} not found.'.format(po_id))
            return Response({'message': 'order information updated successfully', 'status': 200, "data": {"po": update_po}})
        except Exception as e:  # Catch any exceptions during update
            return Response({'message': f'An error occurred: {e}', 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, po_id):
        """
        Deletes a purchase order.

        **DELETE http://127.0.0.1:8000/api/purchase_orders/{po_id}/ **

        This function handles DELETE requests to delete a purchase order with the provided `po_id`.
        """
        # Use the get_object method for consistency
        try:
            delete = self.po_service.delete_order(po_id)
            if not delete:
                raise NotFound('Purchased Order with ID {} not found.'.format(po_id))
            return Response({'message': 'purchased order deleted successfully', 'status': 204}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}', 'status': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
