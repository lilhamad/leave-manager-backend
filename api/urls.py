from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'leaves', views.LeaveViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', ObtainAuthToken.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', views.login),
    path('login', views.login),
    path('leaves/', views.AllLeaves.as_view()),
    path('leaves/<int:id>', views.my_leaves),
    path('leave/<int:id>', views.leave_detail),
    path('create-leave', views.create_leave),
    path('<int:user_id>/leaves/', views.my_leaves, name='employee_leaves'),
]