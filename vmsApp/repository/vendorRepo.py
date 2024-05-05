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
    
    def get_vendor_by_name(self, vendor_name):
        return self.vendor_list.get(name=vendor_name)
    
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
    
    def get_vendor_performance(self, vendor_id):
        vendor = self.get_vendor_by_id(vendor_id)
        # Ensure metrics are up-to-date before serialization
        vendor.calculate_performance_metrics()
        serializer = VendorPerformanceSerializer(vendor)
        return serializer.data
    
    def get_vendor_performance_history(self, vendor_id):
        vendor = self.get_vendor_by_id(vendor_id)
        # Ensure metrics are up-to-date before serialization
        vendor.calculate_performance_metrics()
        serializer = VendorPerformanceSerializer(vendor)
        return serializer.data
    
    def update_vendor_performance(self, vendor_id, vendor_performance):
        vendor = self.get_vendor_by_id(vendor_id)
        vendor.on_time_delivery_rate = vendor_performance['on_time_delivery_rate']
        vendor.average_response_time = vendor_performance['average_response_time']
        vendor.fulfillment_rate = vendor_performance['fulfillment_rate']
        vendor.quality_rating = vendor_performance['quality_rating']
        vendor.save()
        # Trigger performance metric recalculation for the vendor
        vendor.calculate_performance_metrics()
        vendor.save_performance_history()
        return vendor
    
    def create_vendor_performance(self, vendor_id, vendor_performance):
        vendor = self.get_vendor_by_id(vendor_id)
        vendor.on_time_delivery_rate = vendor_performance['on_time_delivery_rate']
        vendor.average_response_time = vendor_performance['average_response_time']
        vendor.fulfillment_rate = vendor_performance['fulfillment_rate']
        vendor.quality_rating = vendor_performance['quality_rating']
        vendor.save()
        # Trigger performance metric recalculation for the vendor
        vendor.calculate_performance_metrics()
        vendor.save_performance_history()
        return vendor
    
    # def delete_vendor_performance(self, vendor_id):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     vendor.on_time_delivery_rate = None
    #     vendor.average_response_time = None
    #     vendor.fulfillment_rate = None
    #     vendor.quality_rating = None
    #     vendor.save()
    #     # Trigger performance metric recalculation for the vendor
    #     vendor.calculate_performance_metrics()
    #     vendor.save_performance_history()
    #     return vendor
    
    # def update_vendor_performance_history(self, vendor_id, vendor_performance_history):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     vendor.on_time_delivery_rate = vendor_performance_history['on_time_delivery_rate']
    #     vendor.average_response_time = vendor_performance_history['average_response_time']
    #     vendor.fulfillment_rate = vendor_performance_history['fulfillment_rate']
    #     vendor.quality_rating = vendor_performance_history['quality_rating']
    #     vendor.save()
    #     # Trigger performance metric recalculation for the vendor
    #     vendor.calculate_performance_metrics()
    #     vendor.save_performance_history()
    #     return vendor
    
    # def create_vendor_performance_history(self, vendor_id, vendor_performance_history):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     vendor.on_time_delivery_rate = vendor_performance_history['on_time_delivery_rate']
    #     vendor.average_response_time = vendor_performance_history['average_response_time']
    #     vendor.fulfillment_rate = vendor_performance_history['fulfillment_rate']
    #     vendor.quality_rating = vendor_performance_history['quality_rating']
    #     vendor.save()
    #     # Trigger performance metric recalculation for the vendor
    #     vendor.calculate_performance_metrics()
    #     vendor.save_performance_history()
    #     return vendor
    
    # def delete_vendor_performance_history(self, vendor_id):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     vendor.on_time_delivery_rate = None
    #     vendor.average_response_time = None
    #     vendor.fulfillment_rate = None
    #     vendor.quality_rating = None
    #     vendor.save()
    #     # Trigger performance metric recalculation for the vendor
    #     vendor.calculate_performance_metrics()
    #     vendor.save_performance_history()
    #     return vendor
    
    # def get_vendor_performance_history_list(self, vendor_id):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     # Ensure metrics are up-to-date before serialization
    #     vendor.calculate_performance_metrics()
    #     serializer = VendorPerformanceSerializer(vendor)
    #     return serializer.data
    
    # def get_vendor_performance_history_by_id(self, vendor_id, vendor_performance_history_id):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     # Ensure metrics are up-to-date before serialization
    #     vendor.calculate_performance_metrics()
    #     serializer = VendorPerformanceSerializer(vendor)
    #     return serializer.data
    
    # def update_vendor_performance_history_by_id(self, vendor_id, vendor_performance_history_id, vendor_performance_history):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     vendor.on_time_delivery_rate = vendor_performance_history['on_time_delivery_rate']
    #     vendor.average_response_time = vendor_performance_history['average_response_time']
    #     vendor.fulfillment_rate = vendor_performance_history['fulfillment_rate']
    #     vendor.quality_rating = vendor_performance_history['quality_rating']
    #     vendor.save()
    #     # Trigger performance metric recalculation for the vendor
    #     vendor.calculate_performance_metrics()
    #     vendor.save_performance_history()
    #     return vendor
    
    # def create_vendor_performance_history_by_id(self, vendor_id, vendor_performance_history_id, vendor_performance_history):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     vendor.on_time_delivery_rate = vendor_performance_history['on_time_delivery_rate']
    #     vendor.average_response_time = vendor_performance_history['average_response_time']
    #     vendor.fulfillment_rate = vendor_performance_history['fulfillment_rate']
    #     vendor.quality_rating = vendor_performance_history['quality_rating']
    #     vendor.save()
    #     # Trigger performance metric recalculation for the vendor
    #     vendor.calculate_performance_metrics()
    #     vendor.save_performance_history()
    #     return vendor
    
    # def delete_vendor_performance_history_by_id(self, vendor_id, vendor_performance_history_id):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     vendor.on_time_delivery_rate = None
    #     vendor.average_response_time = None
    #     vendor.fulfillment_rate = None
    #     vendor.quality_rating = None
    #     vendor.save()
    #     # Trigger performance metric recalculation for the vendor
    #     vendor.calculate_performance_metrics()
    #     vendor.save_performance_history()
    #     return vendor
    
    # def get_vendor_performance_history_list_by_id(self, vendor_id):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     # Ensure metrics are up-to-date before serialization
    #     vendor.calculate_performance_metrics()
    #     serializer = VendorPerformanceSerializer(vendor)
    #     return serializer.data
    
    # def get_vendor_performance_history_by_date(self, vendor_id, date):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     # Ensure metrics are up-to-date before serialization
    #     vendor.calculate_performance_metrics()
    #     serializer = VendorPerformanceSerializer(vendor)
    #     return serializer.data
    
    # def update_vendor_performance_history_by_date(self, vendor_id, date, vendor_performance_history):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     vendor.on_time_delivery_rate = vendor_performance_history['on_time_delivery_rate']
    #     vendor.average_response_time = vendor_performance_history['average_response_time']
    #     vendor.fulfillment_rate = vendor_performance_history['fulfillment_rate']
    #     vendor.quality_rating = vendor_performance_history['quality_rating']
    #     vendor.save()
    #     # Trigger performance metric recalculation for the vendor
    #     vendor.calculate_performance_metrics()
    #     vendor.save_performance_history()
    #     return vendor
    
    # def create_vendor_performance_history_by_date(self, vendor_id, date, vendor_performance_history):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     vendor.on_time_delivery_rate = vendor_performance_history['on_time_delivery_rate']
    #     vendor.average_response_time = vendor_performance_history['average_response_time']
    #     vendor.fulfillment_rate = vendor_performance_history['fulfillment_rate']
    #     vendor.quality_rating = vendor_performance_history['quality_rating']
    #     vendor.save()
    #     # Trigger performance metric recalculation for the vendor
    #     vendor.calculate_performance_metrics()
    #     vendor.save_performance_history()
    #     return vendor
    
    # def delete_vendor_performance_history_by_date(self, vendor_id, date):
    #     vendor = self.get_vendor_by_id(vendor_id)
    #     vendor.on_time_delivery_rate = None
    #     vendor.average_response_time = None
    #     vendor.fulfillment_rate = None
    #     vendor.quality_rating = None
    #     vendor.save()
    #     # Trigger performance metric recalculation for the vendor
    #     vendor.calculate_performance_metrics()
    #     vendor.save_performance_history()
    #     return vendor
    