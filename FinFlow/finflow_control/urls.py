from django.urls import path, include
from . import views

app_name = 'finflow_control'

urlpatterns = [
    path('finflow_info/', views.Finflow_Info, name='finflow_info_setting'),
    path('finflow_control/', views.Finflow_Control, name='finflow_control'),
    
    # path('api/v1/card-save', views.CardSave.as_view(), name='card_save'), 
    path('api/v1/card-check', views.CardCheck.as_view(), name='card_check'), 
    
    path('api/v1/bank-check', views.BankCheck.as_view(), name='bank_check'), 
    
    # path('finflow_control/', views.Finflow_Info.as_view(), name='finflow_control'),    
    # path('finflow_list/', views.Finflow_Info.as_view(), name='finflow_list'),    


    # path('api/v1/card-check-enroll', views.CardCheckEnrollView.as_view(), name='card_check_enroll'), 
    
    # path('api/v1/card-update/<int:pk>', views.CardEdit.as_view(), name='card_edit'), 
    # path('api/v1/card-delete/<int:pk>', views.CardDelete.as_view(), name='card_delete'), 

    # path('enroll/insert', views.insert_card_view, name='insert_card_info'),       
]