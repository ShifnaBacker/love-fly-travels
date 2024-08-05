from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
from io import BytesIO
from .models import Service, Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('service', 'amount', 'currency', 'customer_name', 'customer_email', 'customer_contact_india', 'customer_contact_other', 'feedback', 'status', 'order_id')
    list_filter = ('currency', 'status')
    search_fields = ('customer_name', 'customer_email', 'order_id')

    actions = ['export_to_xls']

    def export_to_xls(self, request, queryset):
        # Create a new workbook and add a worksheet
        wb = Workbook()
        ws = wb.active
        ws.append(['Service', 'Amount', 'Currency', 'Customer Name', 'Customer Email', 'Customer Contact India', 'Customer Contact Other', 'Feedback', 'Status', 'Order ID'])

        # Add the payment data to the worksheet
        for payment in queryset:
            ws.append([
                payment.service.name,
                payment.amount,
                payment.currency,
                payment.customer_name,
                payment.customer_email,
                payment.customer_contact_india,
                payment.customer_contact_other,
                payment.feedback,
                payment.status,
                payment.order_id,
            ])

        # Save the workbook to a BytesIO object
        byte_stream = BytesIO()
        wb.save(byte_stream)
        byte_stream.seek(0)  # Move to the beginning of the BytesIO object

        # Create a response with the Excel file
        response = HttpResponse(
            byte_stream.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=payments.xlsx'
        return response

    export_to_xls.short_description = "Export Selected Payments to XLS"

admin.site.register(Service)
admin.site.register(Payment, PaymentAdmin)
