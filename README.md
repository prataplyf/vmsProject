# Vendor Management System with Performance Metrics
    : This project implements a Vendor Management System using Django and Django REST Framework. 
    : It allows you to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

# Features

## Vendor Profile Management:
    - Create, view, update, and delete vendor profiles.
    - Store essential vendor information including name, contact details, address, and a unique vendor code.

## Purchase Order Tracking:
    - Create, view, update, and delete purchase orders.
    - Track details like PO number, vendor, order date, items, quantity, and status.
    - Filter purchase orders by vendor.

## Vendor Performance Evaluation:
    - Calculate and track vendor performance metrics:
        - On-Time Delivery Rate
        - Quality Rating Average
        - Average Response Time
        - Fulfillment Rate
    - View a vendor's performance metrics through a dedicated API endpoint.

## Data Models
     - Vendor: Stores vendor information and performance metrics.
     - Purchase Order (PO): Captures purchase order details used for performance metric calculations.


## API Endpoints

## Vendor Management:

    - POST  ** /api/vendors/ ** : Create a new vendor.
    - GET  ** /api/vendors/ ** : List all vendors.
    - GET  ** /api/vendors/{vendor_id}/ ** : Retrieve details of a specific vendor.
    - PUT  ** /api/vendors/{vendor_id}/ ** : Update a vendor's details.
    - DELETE  ** /api/vendors/{vendor_id}/ ** : Delete a vendor.

## Purchase Order Management:

    - POST  ** /api/purchase_orders/ ** : Create a new purchase order.
    - GET  ** /api/purchase_orders/ ** : List all purchase orders (with optional vendor filter).
    - GET  ** /api/purchase_orders/{po_id}/ ** : Retrieve details of a specific purchase order.
    - PUT  ** /api/purchase_orders/{po_id}/ ** : Update a purchase order.
    - DELETE  ** /api/purchase_orders/{po_id}/ ** : Delete a purchase order.

## Vendor Performance:

    - GET  ** /api/vendors/{vendor_id}/performance/ ** : Retrieve a vendor's calculated performance metrics.
    - POST  ** /api/purchase_orders/{po_id}/acknowledge/ ** : For vendors to acknowledge POs.
    


# Setup and Usage
1: - Clone the repository

    git clone https://github.com/prataplyf/vmsProject.git

2: - Install Dependencies

    pip install -r requirements.txt

3: - Run database migrations:

    python manage.py makemigrations
    python manage.py migrate

4: - Start the development server:

    python manage.py runserver


# POSTMAN Json API

You can download and import this postman json data to test in your local Postman

    https://github.com/prataplyf/datasets/blob/main/VendorManagementSystem.postman_collection.json

In this I have mentioned all Vendor and Purchase Order related APIs along with the input parameters