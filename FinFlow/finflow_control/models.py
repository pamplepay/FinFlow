import os, hmac, json, time, base64, random, datetime, hashlib, requests

from model_utils.models import TimeStampedModel

from django.utils import timezone
from django.db import models
from django.conf import settings  # User 모델을 참조하기 위해 사용
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CodefToken(models.Model):
    codef_token = models.CharField(max_length=1024, verbose_name="Codef Token")
    
    def __str__(self):
        return str(self.codef_token)
    
    class Meta:
        db_table = "FinFolw_Control_TB"
        verbose_name = "카드정보"
        verbose_name_plural = "카드정보"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class ApprovalCheck(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="사용자")
    approval_date = models.DateField(verbose_name="승인 Request 날짜")
    approval_check = models.BooleanField(default=False, verbose_name="승인 Request 여부")
    

    class Meta:
        db_table = "FinFlow_Approval_Check_TB"
        verbose_name = "승인체크"
        verbose_name_plural = "승인체크"

    def __str__(self):
        return self.commMemberStoreGroup

class StoreGroup(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="사용자")
    commMemberStoreGroup = models.CharField(max_length=255, verbose_name="공동 회원 매장 그룹")

    class Meta:
        db_table = "FinFlow_Store_Group_TB"
        verbose_name = "서비스 이용 거래처 리스트"
        verbose_name_plural = "서비스 이용 거래처 리스트"

    def __str__(self):
        return self.commMemberStoreGroup

class TransactionHistory(models.Model):
    store_group = models.ForeignKey(StoreGroup, on_delete=models.CASCADE, related_name='transactions', verbose_name="매장 그룹")
    resCardCompany = models.CharField(max_length=100, verbose_name="카드 회사")
    resTotalAmount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="총 금액")
    resTotalCount = models.IntegerField(verbose_name="총 거래 횟수")
    resUsedAmount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="사용 금액")
    resCount = models.IntegerField(verbose_name="사용 건수")
    resCancelAmount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="취소 금액")
    resCancelCount = models.IntegerField(verbose_name="취소 건수")

    class Meta:
        db_table = "FinFlow_Transaction_History_TB"
        verbose_name = "거래처 거래 기록"
        verbose_name_plural = "거래처 거래 기록들"

    def __str__(self):
        return f"{self.resCardCompany} - {self.store_group}"

class ApprovalDetail(models.Model):
    transaction = models.ForeignKey(TransactionHistory, on_delete=models.CASCADE, related_name='approval_details', verbose_name="거래 기록")
    resType = models.CharField(max_length=50, verbose_name="거래 유형")
    resAccountTrDate = models.DateField(verbose_name="거래 날짜")
    resAccountTrTime = models.TimeField(verbose_name="거래 시간")
    resCardCompany = models.CharField(max_length=100, verbose_name="카드 회사")
    resCardName = models.CharField(max_length=100, blank=True, verbose_name="카드 명")
    resCardNo = models.CharField(max_length=100, verbose_name="카드 번호")
    resApprovalNo = models.CharField(max_length=100, blank=True, verbose_name="승인 번호")
    resUsedAmount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="사용 금액")
    resInstallmentMonth = models.CharField(max_length=50, verbose_name="할부 개월")

    class Meta:
        db_table = "FinFlow_Approval_Detail_TB"
        verbose_name = "거래처 승인 상세"
        verbose_name_plural = "거래처 승인 상세들"

    def __str__(self):
        return f"{self.resType} - {self.transaction}"
