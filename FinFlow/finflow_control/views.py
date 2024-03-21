import os
import json
import urllib

from .modules import get_token, request_token, check_card, publicRSA
from user.models import User
from .models import CodefToken, StoreGroup, TransactionHistory, ApprovalDetail
# from .restricts import *
from user.decorators import *

from easycodefpy import Codef, ServiceType
from django.conf import settings
from datetime import datetime

from django.shortcuts import render
from django.template.response import TemplateResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from rest_framework import serializers, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

@login_message_required
def Finflow_Info(request):
    if request.user.is_authenticated:
        card_sets = User.objects.filter(user_id = request.user)
        context = {
            'card_sets': card_sets
            }
        return render(request, 'finflow/finflow_info.html',context)    
    else:
        return render(request, 'finflow/finflow_info.html')

@login_message_required
def Finflow_Control(request):
    return render(request, 'finflow/finflow_info.html')

User = get_user_model()

def save_json_to_models(response_text, user):
    
    # URL 인코딩된 문자열을 디코딩
    decoded_text = urllib.parse.unquote_plus(response_text)
    print(decoded_text)
    
    # JSON 데이터 로딩
    data = json.loads(decoded_text)
    
    # StoreGroup 인스턴스 생성 혹은 업데이트
    store_group, _ = StoreGroup.objects.get_or_create(
        user=user,
        defaults={'commMemberStoreGroup': data['data']['commMemberStoreGroup']}
    )
    
    # TransactionHistory 및 ApprovalDetail 인스턴스 생성
    for history in data['data']['resApprovalHistoryList']:
        transaction_history = TransactionHistory.objects.create(
            store_group=store_group,
            resCardCompany=history['resCardCompany'],
            resTotalAmount=history['resTotalAmount'],
            resTotalCount=history['resTotalCount'],
            resUsedAmount=history['resUsedAmount'],
            resCount=history['resCount'],
            resCancelAmount=history['resCancelAmount'],
            resCancelCount=history['resCancelCount']
        )
        
        for detail in history['resApprovalDetailList']:
            ApprovalDetail.objects.create(
                transaction=transaction_history,
                resType=detail['resType'],
                resAccountTrDate=datetime.strptime(detail['resAccountTrDate'], "%Y%m%d").date(),
                resAccountTrTime=datetime.strptime(detail['resAccountTrTime'], "%H%M%S").time(),
                resCardCompany=detail['resCardCompany'],
                resCardName=detail['resCardName'],
                resCardNo=detail['resCardNo'],
                resApprovalNo=detail['resApprovalNo'],
                resUsedAmount=detail['resUsedAmount'],
                resInstallmentMonth=detail.get('resInstallmentMonth', '0')  # 'resInstallmentMonth'가 없는 경우 '0'을 사용
            )
            
### For API views ###
class CardCheck(APIView):
    # 체크 필요. 왜 해당 로직에서 인증에 대해 오류가 발생하는지....
    permission_classes = [IsAuthenticated]
    # authentication_classes = [BasicAuthentication]
    
    def post(self, request):
        try:
            user_id = request.user.user_id
            user_cmpnum = request.user.user_biznum
            card_id = request.POST.get('card_id')
            card_pw = request.POST.get('card_pw')
            
            response = request_token()
            print(response.status_code)
            
            if response.status_code == 200:
                # JSON 문자열을 딕셔너리로 변환
                response_dict = json.loads(response.text)

                # access_token 값 추출
                access_token = response_dict['access_token']
                print(access_token)
                
                # access_token 값으로 CodefToken 인스턴스를 조회
                try:
                    codef_token_instance = CodefToken.objects.first()
                    # 존재하는 토큰의 값과 새로운 값이 다른 경우에만 업데이트
                    if codef_token_instance.codef_token != access_token:
                        codef_token_instance.codef_token = access_token
                        codef_token_instance.save()
                        print("토큰이 업데이트되었습니다.")
                    else:
                        print("토큰 값이 동일하여 업데이트되지 않았습니다.")
                except ObjectDoesNotExist:
                    # 인스턴스가 존재하지 않는 경우 새로 생성
                    CodefToken.objects.create(codef_token=access_token)
                    print("새로운 토큰이 저장되었습니다.")
            else:
                return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
            
            response = check_card(access_token, card_id, card_pw)
            
            print('response.status_code = ' + str(response.status_code))
            print('response.text = ' + urllib.parse.unquote_plus(response.text))
            
            if response.status_code == 200:
                # 현재 로그인한 사용자 인스턴스를 가져옵니다.
                user = request.user
                # card_id와 card_pw를 업데이트합니다.
                user.card_user_id = card_id
                pw = publicRSA(card_pw)
                user.card_user_pw = pw
                # 변경 사항을 저장합니다.
                user.save()
                
                save_json_to_models(response.text, user)
                
                return Response({"message": "Success"}, status=status.HTTP_200_OK)

            else:
                # 오류 응답을 반환합니다.
                return Response({"message": "Failed"}, status=response.status_code)
        
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        
class CardSave(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            card_info = request.data
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

        
class BankCheck(APIView):
    # 체크 필요. 왜 해당 로직에서 인증에 대해 오류가 발생하는지....
    permission_classes = [IsAuthenticated]
    # authentication_classes = [BasicAuthentication]
    
    def post(self, request):
        try:
            user_id = request.user.user_id
            user_cmpnum = request.user.user_biznum
            bank_id = request.POST.get('bank_id')
            bank_pw = request.POST.get('bank_pw')
            bank_num = request.POST.get('bank_num')
            
            
            response = request_token()
            print(response.status_code)
            
            if response.status_code == 200:
                # JSON 문자열을 딕셔너리로 변환
                response_dict = json.loads(response.text)

                # access_token 값 추출
                access_token = response_dict['access_token']
                print(access_token)
                
                # access_token 값으로 CodefToken 인스턴스를 조회
                try:
                    codef_token_instance = CodefToken.objects.first()
                    # 존재하는 토큰의 값과 새로운 값이 다른 경우에만 업데이트
                    if codef_token_instance.codef_token != access_token:
                        codef_token_instance.codef_token = access_token
                        codef_token_instance.save()
                        print("토큰이 업데이트되었습니다.")
                    else:
                        print("토큰 값이 동일하여 업데이트되지 않았습니다.")
                except ObjectDoesNotExist:
                    # 인스턴스가 존재하지 않는 경우 새로 생성
                    CodefToken.objects.create(codef_token=access_token)
                    print("새로운 토큰이 저장되었습니다.")
            else:
                return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
            
            response = check_card(access_token, card_id, card_pw)
            
            print('response.status_code = ' + str(response.status_code))
            print('response.text = ' + urllib.parse.unquote_plus(response.text))
            
            if response.status_code == 200:
                # 현재 로그인한 사용자 인스턴스를 가져옵니다.
                user = request.user
                # card_id와 card_pw를 업데이트합니다.
                user.card_user_id = card_id
                pw = publicRSA(card_pw)
                user.card_user_pw = pw
                # 변경 사항을 저장합니다.
                user.save()
                
                
                
                return Response({"message": "Success"}, status=status.HTTP_200_OK)

            else:
                # 오류 응답을 반환합니다.
                return Response({"message": "Failed"}, status=response.status_code)
        
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)            

