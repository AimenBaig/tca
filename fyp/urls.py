from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.index),
                  path('conversation', views.conversation),
                  path('conversation/index', views.conversation),
                  path('conversation/draft', views.drafts),
                  path('conversation/sent', views.sent),
                  path('conversation/trash', views.trash),
                  path('conversation/create', views.creat_mail),
                  path('user_role', views.user_roles),
                  path('user_role/index', views.user_roles),
                  path('user_role/add', views.add_role),
                  path('user_role/delete/<int:id>', views.delete_role),
                  path('user_role/edit/<int:id>', views.edit_role),
                  path('user_role/update_role/<int:id>', views.update_role),
                  path('dashboard', views.dashboard),
                  path('logout', views.logout),
                  path('users/index', views.users),
                  path('users', views.users),
                  path('users/view/<int:id>', views.view_user),
                  path('users/edit/<int:id>', views.edit_user),
                  path('users/delete/<int:id>', views.delete_user),
                  path('users/add', views.add_user),
                  path('api_settings', views.api_settings),
                  path('api_settings/index', views.api_settings),
                  path('api_settings/add', views.add_api),
                  path('api_settings/edit/<int:id>', views.edit_api),
                  path('api_settings/delete/<int:id>', views.delete_api),
                  path('system_setting', views.system_setting),
                  path('system_setting/index', views.system_setting),
                  path('system_setting/edit/<int:id>', views.system_setting_edit),
                  path('tweets_gathering', views.tweets_gathering),
                  path('twitter_users', views.twitter_users),
                  path('twitter_users/view', views.view_profile),
                  path('analysis', views.analysis),
                  path('analysis_view', views.analysis_view),
                  path('categorization', views.categorization),
                  path('category_analysis', views.category_analysis),
                  path('fake_users', views.faked_account)
                  # path('tweets_gathering')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
