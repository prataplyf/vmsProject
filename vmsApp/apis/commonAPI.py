# import file modules
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..services.commonServices import CommonService

class CommonBaseView(APIView):
    """
    Base class for API views that utilize common functionalities.

    This class serves as a foundation for API views that share common logic or interact
    with a common service layer. It inherits from Django REST framework's `APIView` class
    to leverage its functionalities.

    By inheriting from this class, other API views can access the `common_service` instance
    and utilize its methods for handling common tasks efficiently.
    """


    def __init__(self) -> None:
        """
        Initializes the CommonBaseView instance.

        This constructor establishes a connection with the `common_service` instance API views.
        """
        self.common_service = CommonService()


class OrderAcknowledgeAPI(CommonBaseView):
    """
    API endpoint for acknowledging a purchase order.

    This class handles API requests for acknowledging a purchase order by its ID.
    It inherits from `CommonBaseView` to access the `common_service` instance.
    """

    def post(self, request, po_id):
        """
        Acknowledges a purchase order.

        This function handles POST requests to acknowledge a purchase order with the
        provided `po_id`. It utilizes a try-except block to handle potential exceptions.

        On success (if the purchase order is acknowledged), it returns a JSON response
        containing a success message and a status code of 200 (OK).

        On failure (including cases where the purchase order is not found), it returns
        a JSON response with an error message and a status code of 404 (Not Found).
        """
        try:
            ack_status = self.common_service.get_acknowledged_purchase_orders(po_id)
            if not ack_status:
                raise Exception(f"failed to acknowledge purchase order id: {po_id}")
            if ack_status == 1:
                return Response({'message': 'Purchase order acknowledged successfully', 'status': 200}, status=status.HTTP_200_OK)
            
            return ack_status
        except Exception as e:
            return Response({'message': 'failed to acknowledged purchase order', 'status': 404}, status=status.HTTP_404_NOT_FOUND)



class CompletePurchaseOrderAPI(CommonBaseView):
    def post(self, request, po_id):
        """
        Marks a purchase order as complete.

        This function handles POST requests to mark a purchase order with the provided `po_id`
        as complete. It utilizes a try-except block to handle potential exceptions.

        On success (if the purchase order is marked complete), it returns a JSON response
        containing a success message and a status code of 200 (OK).

        On failure (including cases where the purchase order is not found), it returns
        a JSON response with an error message and a status code of 404 (Not Found).
        """
        try:
            po_complete_status = self.common_service.completed_purchase_orders(po_id)
            if not po_complete_status:
                raise Exception(f"failed to update complete status of purchase order id: {po_id}")
            if po_complete_status == 1:
                return Response({'message': 'Purchase order completed successfully'}, status=status.HTTP_200_OK)
            
            return po_complete_status
        except Exception as e:
            return Response({'message': 'failed to complete purchase order', 'status': 404}, status=status.HTTP_404_NOT_FOUND)



class UpdatePurchaseOrderQualityRatingAPI(CommonBaseView):
    def patch(self, request, po_id):
        """
        Updates the quality rating of a purchase order.

        This function handles PATCH requests to update the quality rating of a purchase order
        with the provided `po_id`. It expects the quality rating information in the request body.
        It utilizes a try-except block to handle potential exceptions.

        On success (if the quality rating is updated), it returns a JSON response containing
        a success message and a status code of 200 (OK).

        On failure (including cases where the purchase order is not found or the update fails),
        it returns a JSON response with an error message and a status code of 404 (Not Found).
        """
        try:
            po_quality_rating_status = self.common_service.update_quality_rating(po_id, request.data)
            if not po_quality_rating_status:
                raise Exception(f"failed to update quality rating of purchase order id: {po_id}")
            return Response({'message': 'Purchase order quality rating updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'failed to update quality rating to vendors on item purchased', 'status': 404}, status=status.HTTP_404_NOT_FOUND)

