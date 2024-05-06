# import required modules
from ..models import Vendor
from ..serializers import VendorSerializer, VendorPerformanceSerializer

class VendorRepository:

    def __init__(self):
        self.vendor_list = Vendor.objects.all()
    
    def get_all_vendors(self):
        return Vendor.objects.all()
    
    def get_vendor_by_id(self, vendor_id):
        return Vendor.objects.get(pk=vendor_id)
    
    def create_vendor(self, vendor_name):
        vendor = Vendor(name=vendor_name)
        vendor.save()
        return vendor
    
    def update_vendor(self, vendor_id, vendor_name):
        vendor = self.get_vendor_by_id(vendor_id)
        vendor.name = vendor_name
        vendor.save()
        return vendor
    
    def delete_vendor(self, vendor_id):
        vendor = self.get_vendor_by_id(vendor_id)
        if not vendor:
            return None
        vendor.delete()
        return vendor
    
