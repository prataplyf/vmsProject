import uuid
from django.db import models
from django.utils import timezone
from .constants.appConstants import STATUS_CHOICES


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Vendor(BaseModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=100)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
    def calculate_performance_metrics(self):
        completed_pos = self.purchase_orders.all()  # Consider all purchase orders

        if not completed_pos.exists():
            return  # Handle scenario with no POs (avoid division by zero)

        total_pos = completed_pos.count()

        # On-Time Delivery Rate
        on_time_deliveries = completed_pos.filter(delivery_date__gte=models.F('issue_date'), status='completed')
        self.on_time_delivery_rate = (on_time_deliveries.count() / total_pos) * 100  # Percentage

        # Quality Rating Average (assuming quality_rating is a field in PurchaseOrder)
        quality_ratings = [po.quality_rating for po in completed_pos if po.quality_rating is not None]
        self.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0

        # Average Response Time (based on provided logic)
        acknowledged_pos = completed_pos.filter(acknowledgment_date__isnull=False)
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() / 86400 for po in acknowledged_pos]
        self.average_response_time = sum(response_times) / len(response_times) if response_times else 0

        # Fulfillment Rate (refer to previous explanation)
        successful_pos = completed_pos.filter(status='completed')  # Filter completed POs
        self.fulfillment_rate = (successful_pos.count() / total_pos) * 100  # Percentage

        self.save()

    def save_performance_history(self):
        # Calculate metrics using the logic in calculate_performance_metrics
        performance_data = {
            'on_time_delivery_rate': self.on_time_delivery_rate,
            'quality_rating_avg': self.quality_rating_avg,
            'average_response_time': self.average_response_time,
            'fulfillment_rate': self.fulfillment_rate,
        }
        # Create a new HistoricalPerformance record with calculated metrics
        HistoricalPerformance.objects.create(vendor=self, **performance_data)

    

class PurchaseOrder(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_orders')
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(blank=True, null=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(blank=True, null=True)
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"PO #{self.po_number} - {self.vendor}"
    
    def save(self, *args, **kwargs):
        # Trigger performance metric calculation and history update
        self.vendor.calculate_performance_metrics()
        super().save(*args, **kwargs)


class HistoricalPerformance(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_performance')
    date = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"Performance for {self.vendor} on {self.date}"

