from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/login.html'), name='logout'),
    path('addtask/', views.addTask, name='addtask'),
    path('updatephase/<int:id>', views.updatePhase, name='updatephase'),
    path('updatetask/<int:id>', views.updateTask, name='updatetask'),
    path('deletetask/<int:id>', views.deleteTask, name='deletetask'),
]