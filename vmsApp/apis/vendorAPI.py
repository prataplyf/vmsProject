# import file modules
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ..services.vendorServices import VendorService

class VendorBaseView(APIView):
    """
    Base class for all Vendor API views. Provides access to the VendorService instance.

    This class serves as the foundation for all API views related to vendors in the application.
    It inherits from Django REST framework's `APIView` class to leverage its functionalities.

    Key features of this base class include:

    - Access to the `vendor_service` instance: This instance provides methods for interacting
      with vendor data, such as retrieving, creating, updating, and deleting vendors.

    By inheriting from this class, other vendor-related API views can access the `vendor_service`
    instance and utilize its methods for handling vendor data efficiently.
    """

    def __init__(self) -> None:
        self.vendor_service = VendorService()


class VendorListAPI(VendorBaseView):
    """
    API endpoint for retrieving a list of all vendors and creating new vendors.

    This class provides views for managing the list of vendors in the application.
    It inherits from the `VendorBaseView` class to access the `vendor_service` instance.
    """

    def get(self, request):
        """
        Retrieves a list of all vendors.

        This function retrieves a list of all vendors available in the application. 
        It utilizes a try-except block to handle potential exceptions during retrieval.

        On success, it returns a JSON response containing a list of vendor data,
        a success message, and a status code of 200 (OK).

        On failure, it returns a JSON response with an error message and a status code of 500 (Internal Server Error).
        """
        try:
            all_vendors = self.vendor_service.get_all_vendors()
            if not all_vendors:
                raise Exception("Failed to fetch all vendors")
            return Response(
                {
                    'message': 'Successfully fetched all vendor records',
                    'status': 200,
                    "data": {"vendor": all_vendors.data},
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {'message': f'An error occurred: {str(e)}', 'status': 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """
        Creates a new vendor.

        This function creates a new vendor using the data provided in the request body.
        It utilizes a try-except block to handle potential exceptions during creation.

        On success, it returns a JSON response containing the newly created vendor data,
        a success message, and a status code of 201 (Created).

        On failure, it returns a JSON response with an error message and a status code of 500 (Internal Server Error).
        """
        try:
            vendor = self.vendor_service.create_vendor(request.data)
            if not vendor:
                raise Exception("Failed to create new vendor")
            return Response(
                {
                    'message': 'Vendor created successfully',
                    'status': 201,
                    "data": {"vendor": vendor.data},
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {'message': f'An error occurred: {str(e)}', 'status': 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VendorViewsAPI(VendorBaseView):
    """
    API endpoint for retrieving, updating, and deleting a specific vendor.

    This class provides views for handling requests related to a specific vendor.
    It inherits from the `VendorBaseView` class to access the `vendor_service` instance.
    """

    def get(self, request, vendor_id):
        """
        Retrieves a specific vendor's details.

        This function retrieves a vendor's details using the provided vendor ID.
        It utilizes a try-except block to handle potential exceptions,
        including cases where the vendor is not found.

        On success, it returns a JSON response containing the retrieved vendor data,
        a success message, and a status code of 200 (OK).

        On failure (including cases where the vendor is not found), it returns a JSON
        response with an error message and a status code of 404 (Not Found).
        """
        try:
            vendor = self.vendor_service.get_vendor_details(vendor_id)
            if vendor is None:
                raise NotFound(f"Vendor with ID {vendor_id} not found.")

            return Response(
                {
                    'message': 'Successfully fetched vendor record',
                    'status': 200,
                    "data": {"vendor": vendor.data},
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {'message': f'An error occurred: {str(e)}', 'status': 404},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request, vendor_id):
        """
        Updates a vendor's details.

        This function updates a vendor's details using the provided vendor ID
        and data from the request body. It utilizes a try-except block to handle
        potential exceptions, including cases where the vendor is not found.

        On success, it returns a JSON response containing the updated vendor data,
        a success message, and a status code of 200 (OK).

        On failure (including cases where the vendor is not found), it returns a JSON
        response with an error message and a status code of 400 (Bad Request).
        """
        try:
            vendor = self.vendor_service.update_vendor(vendor_id, request.data)
            if not vendor:
                raise NotFound(f"Vendor with ID {vendor_id} not found.")

            return Response(
                {'message': 'Vendor information updated successfully', 'status': 200, "data": {"vendor": vendor.data}},
            )
        except Exception as e:
            return Response(
                {'message': f'An error occurred: {str(e)}', 'status': 400},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, vendor_id):
        """
        Deletes a vendor.

        This function deletes a vendor using the provided vendor ID. It utilizes a
        try-except block to handle potential exceptions, including cases where the
        vendor is not found.

        On success, it returns a JSON response with a success message and a status
        code of 204 (No Content).

        On failure (including cases where the vendor is not found), it returns a JSON
        response with an error message and a status code of 500 (Internal Server Error).
        """
        try:
            self.vendor_service.delete_vendor(vendor_id)
            return Response({'message': 'Vendor record deleted successfully', 'status': 204}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {'message': f'An error occurred: {str(e)}', 'status': 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VendorPerformanceView(VendorBaseView):
    """
    API endpoint for retrieving vendor performance.
    """

    def get(self, request, vendor_id):
        """
        Retrieves a specific vendor's performance data.

        This function retrieves a vendor's performance data using the provided vendor ID.
        It utilizes a try-except block to handle potential exceptions.

        On success, it returns a JSON response containing the retrieved vendor performance 
        data, a success message, and a status code of 200 (OK).

        On failure (including cases where the vendor is not found), it returns a JSON 
        response with an error message and a status code of 404 (Not Found).
        """
        try:
            vendor = self.vendor_service.get_vendor_performance(vendor_id)
            if vendor is None:
                raise NotFound(f"Vendor with ID {vendor_id} not found.")

            return Response(
                {
                    'message': 'Vendor performance fetched successfully',
                    'status': 200,
                    "data": {"vendor": vendor.data},
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {'message': f'An error occurred: {str(e)}', 'status': 404},
                status=status.HTTP_404_NOT_FOUND,
            )

