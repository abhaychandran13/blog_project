from . import views
from django.urls import path, include

app_name = 'blogapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('viewall/<int:pk>/', views.viewall, name='viewall'),
    path('myblogs/', views.myblogs, name='myblogs'),
    path('submit/', views.submit, name='submit'),
    path('update/<int:post_id>/', views.update, name='update'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('logout', views.logout, name='logout'),

    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:post_id>/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),

]
