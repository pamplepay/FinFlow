# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
#
import requests, json, base64, os
import urllib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5

from easycodefpy import Codef, ServiceType, encrypt_rsa
from django.conf import settings

# Codef 접속 서버 정보
# https://development.codef.io
# https://api.codef.io

# ========== Encode string data  ==========
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')
# ========== Encode string data  ==========

# ========== HTTP 기본 함수 ==========
def http_sender(url, token, body):
    headers = {'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
        }

    response = requests.post(url, headers = headers, data = urllib.parse.quote(str(json.dumps(body))))

    # print('response.status_code = ' + str(response.status_code))
    # print('response.text = ' + urllib.parse.unquote_plus(response.text))

    return response
# ========== HTTP 함수  ==========

# ========== codef key get 함수  ==========
def request_codefjson():
    BASE_DIR = getattr(settings, 'BASE_DIR', None)
    file_path = "codef.json" # 네이버 sens api key 파일
        
    with open(os.path.join(BASE_DIR,file_path), encoding='utf-8') as f:
        codef_key = json.load(f)
        
    return codef_key

def codefkey_clientid():
    codef_key = request_codefjson()
    
    return codef_key['client_id']

def codefkey_clientsecret():
    codef_key = request_codefjson()
    
    return codef_key['client_secret']

def codefkey_publickey():
    codef_key = request_codefjson()
    
    return codef_key['Public_KEY']
# ========== codef key get 함수  ==========

# ========== 비밀번호 암호화  ==========
def publicEncRSA(publicKey, data):
    pubkey = codefkey_publickey()
    
    keyDER = base64.b64decode(pubKey)
    keyPub = RSA.importKey(keyDER)
    cipher = Cipher_PKCS1_v1_5.new(keyPub)
    cipher_text = cipher.encrypt(data.encode())

    encryptedData = base64.b64encode(cipher_text)
    print('encryptedData = ' + encryptedData)

    return encryptedData

def publicRSA(data):
    pwd = encrypt_rsa(data, codefkey_publickey())
    print(pwd)
    
    return pwd
# ========== 비밀번호 암호화  ==========

# ========== Toekn 재발급  ==========
def request_token():
    # token URL
    token_url = 'https://oauth.codef.io/oauth/token'
            
    
    demo_client_id = codefkey_clientid()
    demo_client_secret = codefkey_clientsecret()
    
    # 상용화 client id & secret key
    # client_id = ''
    # client_secret = ''

    public_key = codefkey_publickey()
    
    authHeader = stringToBase64(demo_client_id + ':' + demo_client_secret).decode("utf-8")

    headers = {
        'Acceppt': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + authHeader
        }

    response = requests.post(token_url, headers = headers, data = 'grant_type=client_credentials&scope=read')

    return response
# ========== Toekn 재발급  ==========

# ========== 여신협회 id/pw 체크 함수  ==========
def check_card(access_token, card_id, card_pw):
    # Demo URL
    url = 'https://development.codef.io/v1/kr/card/a/cardsales/daily-approval-details'    
    # 정식 URL
    # url = 'https://api.codef.io/v1/kr/card/a/cardsales/daily-approval-details'
    
    # id = "pample"
    # pw = "ZW8Nu9RkAfgQO1v1vRA0dxZP58+ASZDFhd76u5Uf0yErau1Xsu88zAItr8vbbikIRW+kqauCsSoWda4Zxf3bWJJdHzV63j2zeIVJRqWxtXoW/YvsA5SSlni/qHKK8SsVcsGFo28sCFyDstTaXEDoZTZa8Rdx3gdaILJ2VOBMWR4RE3elmZFPXBEuDNevH7EaWo1Kd4sBKgvCyqi6XL3YIcM4dmHBA3BaKFh37edmvzG8NfTvaZLzySg+XJRvNPoZaN3lTAHzqb640WhpNE0V4y5MnV11yvfAXVv+k8iX++ZUiCXYBt88pSLo4OHnf4sOnZrNwH7k+WQ1SYZaOSIQbg=="
    # card_pw = 'pmplus0101**'
    
    id = card_id    
    pw = publicRSA(card_pw)
    print(pw)
    
    body = {
	"organization": "0323",
	"id": id,
    "password" : pw,
    "startDate" : "20240320",
    # "endDate" : "20240229",
    "memberStoreGroup" : "",
    "cardCompany" :"",
    "memberStoreNo" : "",
    "orderBy" : "",
    "inquiryType" : ""
    }
    
    response = http_sender(url, access_token, body)    
    
    return response
    
# ========== 여신협회 id/pw 체크 함수  ==========

def get_token():    
    BASE_DIR = getattr(settings, 'BASE_DIR', None)
    file_path = "codef.json" # 네이버 sens api key 파일
        
    with open(os.path.join(BASE_DIR,file_path), encoding='utf-8') as f:
            codef_key = json.load(f)
        
        
    demo_client_id = codef_key['client_id']
    demo_client_secret = codef_key['client_secret']
    
    # 상용화 client id & secret key
    # client_id = ''
    # client_secret = ''

    public_key = codef_key['Public_KEY']

    # 코드에프 인스턴스 생성
    codef = Codef()
    codef.public_key = public_key

    # 데모 클라이언트 정보 설정
    # - 데모 서비스 가입 후 코드에프 홈페이지에 확인 가능(https://codef.io/#/account/keys)
    # - 데모 서비스로 상품 조회 요청시 필수 입력 항목
    codef.set_demo_client_info(demo_client_id, demo_client_secret)

    # 정식 클라이언트 정보 설정
    # - 정식 서비스 가입 후 코드에프 홈페이지에 확인 가능(https://codef.io/#/account/keys)
    # - 정식 서비스로 상품 조회 요청시 필수 입력 항목
    # codef.set_client_info(client_id, client_secret)

    # 토큰 발급 요청
    token = codef.request_token(ServiceType.DEMO)
    
    # 결과 출력
    print(token)
    
    return token

# def test_request_token():
#     codef = Codef()
#     service_type = ServiceType.SANDBOX
#     # 발급 받은 토큰은 자동 셋팅된다
#     token = codef.request_token(service_type)
#     assert codef.get_access_token(service_type) == token

#     # 아직 유요한 토큰이라면 보유하고 있는 토큰을 반환한다
#     new_token = codef.request_token(service_type)
#     assert token == new_token

#     # 만료된 토큰이라면 새로운 토큰을 발급받는다
#     expired_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2aWNlX3R5cGUiOiIyIiwic2NvcGUiOlsicmVhZCJdLCJzZXJ2aWNlX25vIjoiMDAwMDAwMDAwMDAwIiwiZXhwIjoxNjAxNDQ0OTc5LCJhdXRob3JpdGllcyI6WyJSRUxBWSJdLCJqdGkiOiI4NjRhMDcwOS1jNTM2LTQyZTQtOTg0Ni0wMmZlZTk4NTE5OWYiLCJjbGllbnRfaWQiOiI1MDM4YTYzNS00ZjJkLTQ2MDUtOTI1ZS0wMTk5MDM1MTIyYjgifQ.QdviRdu0gBOYHhVlX-X0CE20lfrfVWC-teZlIYKPMqh-TL5odP8WjSSwEkK8SupFmo7BpgSZEVaYPvzY5R6700RKODHBQm-zZuxDNMn4xEGhOvw9IBo8aJerpfas0dxD5HeauNf_nE0wt3MrHNfu1g0FCWyOBTcdeGa3LGc5StP42r--DIShrhV1EyWGqOmTHL-Bl6VdedV59-_yLeD-pxFd0tpF5pwuFBaB_KHt5wGpjkWcRbYGW1dV-_0cwmKbf1Afq2iO633QEibBIA22cIndCTL1zq2qgeS71cINOb0ZTX4-bS5mpUfpkYtvLGLG-f51d_nTzdMz2LR7ojIuXw'
#     codef.set_access_token(expired_token, service_type)
#     new_token = codef.request_token(service_type)
#     assert expired_token != new_token
#     assert expired_token != codef.get_access_token(service_type)

# def get_RSA_pw():