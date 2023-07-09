from django.urls import path
from . import views

urlpatterns = [
    path('', views.ToDoListView.as_view(), name="get list"),
    path('details/<int:pk>', views.ToDoListDetailsView.as_view(), name="details"),
    path('<int:pk>/active', views.activeView, name="active"),
    path('getdata/', views.getData),
    # path('<int:id>/delete', views.deleteItemView, name='delete'),
    # path('test/', views.testAction),
    # path('delete/', views.deleteItem, name='delete item',)
]