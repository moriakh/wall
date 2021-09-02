from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name = "index"),
    path('wall', views.wall, name = "wall"),
    path('new_message', views.new_message, name = "new_message"),
    path('new_comment/<int:message_id>', views.comment, name = "comment"),
    path('destroy/<int:message_id>', views.destroy_message, name = "destroy_message"),
    path('destroy/<int:comment_id>', views.destroy_comment, name = "destroy_comment"),
    path('register', views.register, name = "register"),
    path('login', views.login, name = "login"),
    path('logout', views.logout, name = "logout")
]
