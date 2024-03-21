from django.contrib import admin

from .models import CodefToken, StoreGroup, TransactionHistory, ApprovalDetail

class CodefTokenAdmin(admin.ModelAdmin):
    list_display = (
        'codef_token', 
        )
    # search_fields = ('user_id',)

# StoreGroup 모델을 위한 Admin 클래스
class StoreGroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'commMemberStoreGroup')
    search_fields = ('commMemberStoreGroup',)

# TransactionHistory 모델을 위한 Admin 클래스
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('store_group', 'resCardCompany', 'resTotalAmount', 'resTotalCount', 'resUsedAmount', 'resCount', 'resCancelAmount', 'resCancelCount')
    list_filter = ('store_group', 'resCardCompany')
    search_fields = ('store_group__commMemberStoreGroup', 'resCardCompany')

# ApprovalDetail 모델을 위한 Admin 클래스
class ApprovalDetailAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'resType', 'resAccountTrDate', 'resAccountTrTime', 'resCardCompany', 'resCardName', 'resCardNo', 'resApprovalNo', 'resUsedAmount', 'resInstallmentMonth')
    list_filter = ('transaction__store_group', 'resCardCompany')
    search_fields = ('transaction__store_group__commMemberStoreGroup', 'resCardCompany', 'resCardName')

admin.site.register(CodefToken, CodefTokenAdmin)
admin.site.register(StoreGroup, StoreGroupAdmin)
admin.site.register(TransactionHistory, TransactionHistoryAdmin)
admin.site.register(ApprovalDetail, ApprovalDetailAdmin)
# Register your models here.
