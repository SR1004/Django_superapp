"""
URL configuration for superapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from spapp import views
from spapp.views import expense_tracker

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('tetris/',views.tetris),
    path('calendar/',views.calendar),
    path('calculator/',views.calculator),
    path('food/',views.food),
    path('chatbot/',views.chatbot_view),
    # path('stock/', views.stock_chart),
    path('stock/', views.stock_chart, name="stock_chart"),
    path('stock/<str:symbol>/', views.stock_chart, name="stock_chart_dynamic"),
    path('stock/api/<str:symbol>/', views.stock_data_api, name="stock_data_api"),
    path('weather/', views.weather),
    path('map/',views.map),
    path('diary/',views.diary),
    path('todolist/',views.todolist),
    path('expense/', views.expense_tracker, name='expense_tracker'),
    path('datamanage/',views.datamanage, name='home'),
    path('datamanage/insert/',views.insert),
    path('datamanage/update/<int:id>/',views.update),
    path('datamanage/delete/',views.delete, name='delete_data'),
    path('datamanage/output/<int:id>/',views.see)
]
