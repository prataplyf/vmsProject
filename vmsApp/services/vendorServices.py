# import required modules
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from ..repository.vendorRepo import VendorRepository
from ..serializers import VendorSerializer, VendorPerformanceSerializer

class VendorService:
    """
    Service class for handling vendor data operations.

    This class provides methods for interacting with vendor data, such as retrieving,
    creating, updating, and deleting vendors.
    """

    def __init__(self):
        """
        Initializes the VendorService instance.

        This constructor establishes a connection with the `VendorRepository` instance,
        which likely handles persistence logic for vendor data (e.g., database access).
        """
        self.vendorRepo = VendorRepository()

    def get_all_vendors(self) -> VendorSerializer:
        """
        Retrieves a list of all vendors.

        This function fetches a list of all vendors from the vendor repository.
        """
        try:
            vendors = self.vendorRepo.get_all_vendors()
            serializer = VendorSerializer(vendors, many=True)
            return serializer
        except Exception as e:
            # Consider returning a more informative value or raising a specific exception
            return None

    
    def create_vendor(self, vendor_data):
        """
        Creates a new vendor.

        This function creates a new vendor using the provided vendor data.
        """
        try:
            serializer = VendorSerializer(data=vendor_data)
            if not serializer.is_valid():
                raise serializers.ValidationError(serializer.errors)
            
            serializer.save()
            return serializer
        except Exception as e:  # Catch any exceptions during creation
            return None
    
    def get_vendor_details(self, vendor_id):
        """
        Retrieves a specific vendor's details.

        This function retrieves the details of a vendor using the provided vendor ID.
        """
        try:
            vendor = self.vendorRepo.get_vendor_by_id(vendor_id)
            if not vendor:
                raise NotFound(f"Vendor with ID {vendor_id} not found")

            serializer = VendorSerializer(vendor)
            return serializer
        except Exception as e:  # Catch any exceptions during retrieval
            return None
    
    def update_vendor(self, vendor_id, vendor_data):
        """
        Updates a vendor's details.

        This function updates a vendor's details using the provided vendor ID and data.

        Args:
            vendor_id (int): The ID of the vendor to update.
            vendor_data (dict): The data containing the updated vendor information.

        Returns:
            VendorSerializer: The updated vendor data serialized.
        """

        try:
            vendor = self.vendorRepo.get_vendor_by_id(vendor_id)
            if not vendor:
                raise NotFound(f"Vendor with ID {vendor_id} not found")

            serializer = VendorSerializer(vendor, data=vendor_data)
            if not serializer.is_valid():
                raise serializers.ValidationError(serializer.errors)

            serializer.save()
            return serializer

        except Exception as e:
            print(f"error: {e}")
            return None
    
    def delete_vendor(self, vendor_id):
        """
        Deletes a vendor.

        This function deletes a vendor using the provided vendor ID.
        """
        try:
            vendor = self.vendorRepo.delete_vendor(vendor_id)
            if not vendor:
                raise NotFound(f"Vendor with ID {vendor_id} not found")
            return vendor
        except Exception as e:  # Catch any exceptions during deletion
            return None
    
    def get_vendor_performance(self, vendor_id):
        """
        Retrieves a specific vendor's performance data.

        This function retrieves the performance data of a vendor using the provided vendor ID.
        """
        try:
            vendor = self.vendorRepo.get_vendor_by_id(vendor_id)
            if not vendor:
                raise NotFound(f"Vendor with ID {vendor_id} not found")

            serializer = VendorPerformanceSerializer(vendor)
            return serializer
        except Exception as e:  # Catch any exceptions during retrieval
            return None
    
