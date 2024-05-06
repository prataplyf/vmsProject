# import file modules
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ..services.vendorServices import VendorService

class VendorBaseView(APIView):
    """
    Base class for all Vendor API views. Provides access to the VendorService instance.
    Key features of this base class include:

    - Access to the `vendor_service` instance: This instance provides methods for interacting
      with vendor data, such as retrieving, creating, updating, and deleting vendors.
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
        
        **GET http://127.0.0.1:8000/api/vendors/**

        This function retrieves a list of all vendors available in the application.
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
        **POST http://127.0.0.1:8000/api/vendors/**
        This function creates a new vendor using the data provided in the request body.
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
    """

    def get(self, request, vendor_id):
        """
        Retrieves a specific vendor's details.
        ** GET http://127.0.0.1:8000/api/vendors/{vendor_id}/ **
        This function retrieves a vendor's details using the provided vendor ID.
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
        ** PUT http://127.0.0.1:8000/api/vendors/{vendor_id}/ **
        This function updates a vendor's details using the provided vendor ID
        and data from the request body.
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
        ** DELETE http://127.0.0.1:8000/api/vendors/{vendor_id}/ **
        This function deletes a vendor using the provided vendor ID.
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
        ** GET http://127.0.0.1:8000/api/vendors/{vendor_id}/performance/ **
        This function retrieves a vendor's performance data using the provided vendor ID.
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

