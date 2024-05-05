from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ..models import PurchaseOrder
from django.utils import timezone
from ..services.purchaseOrderServices import PurhaseOrderService

class POBaseModel(APIView):
    """
    Base class for API views related to purchase orders.

    This class serves as a foundation for API views that deal with purchase orders.
    It inherits from Django REST framework's `APIView` class to leverage its functionalities.

    By inheriting from this class, other purchase order-related API views can access
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
    It inherits from `POBaseModel` to access the `po_service` instance.

    **GET /purchase_orders**

    Returns a JSON response containing a list of all purchase orders and a success message
    upon successful retrieval. On failure, it returns an error message with an appropriate
    HTTP status code.
    """
  
    def get(self, request):
        """
        Retrieves a list of all purchase orders.

        This function handles GET requests to retrieve all purchase orders.
        It utilizes a try-except block to handle potential exceptions during retrieval.

        On success, it returns a JSON response containing a list of purchase orders
        (potentially with pagination information), a success message, and a status code of 200 (OK).

        On failure, it returns a JSON response with an error message and a status code of 500
        (Internal Server Error). Consider using more specific exception types and status codes
        for better error handling.
        """
        try:
            po_list = self.po_service.get_all_orders()
            return Response({'message': 'Successfully fetched purchased order records', 'status': 200, "data": {"po": po_list}}, status=status.HTTP_200_OK)
        except Exception as e:  # Catch any exceptions during retrieval
            return Response({'message': f'An error occurred: {str(e)}', 'status': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def post(self, request):
        """
        Creates a new purchase order.

        This function handles POST requests to create a new purchase order. It expects the
        purchase order details in the request body. It utilizes a try-except block to handle
        potential exceptions during creation.

        On success (if the purchase order is created), it returns a JSON response containing
        a success message, the newly created purchase order data (`po_status`), and a status code
        of 201 (Created).

        On failure (including cases where validation errors occur), it returns a JSON response with
        an error message, a more specific status code (e.g., 400 Bad Request for validation errors),
        and potentially detailed error information (`f"{e}"` might reveal more than intended).
        Consider using a serializer class for validation and returning more user-friendly error messages.
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

        **GET /purchase_orders/{po_id}**

        This function handles GET requests to retrieve a purchase order with the provided `po_id`.
        It utilizes a try-except block to handle potential exceptions during retrieval.

        Args:
            request: The incoming HTTP request object.
            po_id (int): The ID of the purchase order to retrieve.

        Output:
            JSON response:
                On success (if the purchase order is found), it returns a JSON response containing
                a success message, the retrieved purchase order details, and a status code of 200 (OK).
                On failure (including cases where the purchase order is not found), it returns
                a JSON response with an error message and a status code of 404 (Not Found).

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

        **PUT /purchase_orders/{po_id}**

        This function handles PUT requests to update a purchase order with the provided `po_id`.
        It expects the update details in the request body. It utilizes a try-except block to handle
        potential exceptions during update.

        Args:
            request: The incoming HTTP request object.
            po_id (int): The ID of the purchase order to update.

        Output:
            JSON response:
                On success (if the purchase order is found and updated), it returns a JSON response
                containing a success message, the updated purchase order details, and a status code
                of 200 (OK).
                On failure (including cases where the purchase order is not found or update fails),
                it returns a JSON response with an error message and a status code of 400 (Bad Request).
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

        **DELETE /purchase_orders/{po_id}**

        This function handles DELETE requests to delete a purchase order with the provided `po_id`.
        It utilizes a try-except block to handle potential exceptions during deletion.

        Args:
            request: The incoming HTTP request object.
            po_id (int): The ID of the purchase order to delete.

        Output:
            JSON response:
                On success (if the purchase order is found and deleted), it returns a JSON response
                with a success message and a status code of 204 (No Content).
                On failure (including cases where the purchase order is not found or update fails),
                it returns a JSON response with an error message and a status code of 400 (Bad Request).
        """
        # Use the get_object method for consistency
        try:
            delete = self.po_service.delete_order(po_id)
            if not delete:
                raise NotFound('Purchased Order with ID {} not found.'.format(po_id))
            return Response({'message': 'purchased order deleted successfully', 'status': 204}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}', 'status': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
