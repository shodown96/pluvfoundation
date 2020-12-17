from django.contrib import admin
from .models import Payment
from .views import verify
from django.contrib import messages
# Register your models here.
def admin_verify_payment(modeladmin, request, queryset):
    count = 0
    negcount = queryset.count() - count
    abandoned = []
    for x in queryset:
        if verify(request,x.id):
            count += 1
            x.paid = True
        else:
            abandoned.insert(x.email)
    if count > 0:
        messages.success(request, count+' Payments were successful')
        messages.warning(request, negcount+' Payments were abandoned or unsuccessful')


admin_verify_payment.short_description = "Verify Payments"

class PaymentAdmin(admin.ModelAdmin):
    actions = [admin_verify_payment]
    list_display = ['email', 'amount', 'paid_at', 'status', 'reference']
    list_filter = ['amount', 'status']

admin.site.register(Payment,PaymentAdmin)



