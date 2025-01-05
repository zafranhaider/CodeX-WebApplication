from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    path('', views.index, name='index'),  
    path('contact/', views.contact_view, name='contact'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('pack/', views.Pack, name='pack'),
    path('do/', views.do, name='do'),
    path('about/', views.about, name='about'),
    path('portfolio/', views.Port, name='portfolio'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('portfolio2', views.portf, name='portfolio2'),
    path('contacts/', views.contact_view2, name='contact_view2'),
    path('feedback/upload/', views.feedback_upload, name='feedback_upload'),
    # Add more routes here
]