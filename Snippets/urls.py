from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from MainApp import views


urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='snippets-add'),
    path('snippets/list', views.snippets_page, name='snippets-list'),
    path('snippets/list/my', views.snippets_page_my, name='my-snippets-list'),
    path('snippet/<int:snippet_id>', views.snippet_detail, name='snippet-detail'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('reg/>', views.reg_page, name='reg'),
 ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

