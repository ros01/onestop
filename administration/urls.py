from django.urls import path
from . import views
from .views import (
    DashboardView,
    FileView,
    AllFiles,
    FilesGroupView,
    FilesListView,
    StarredFiles,
    SharedFiles,
    SharedOutgoing,
    SharedLinks,
    RecoverFiles,
    FileSettings,
    IndexView,
    MailBox,
    Messages,
    Chats,
    Calendar,
    

   
)


app_name = 'administration'

urlpatterns = [
	path('administration_dashboard/', DashboardView.as_view(), name='administration_dashboard'),
	path('index/', IndexView.as_view(), name='index'),
	path('filemanager_dashboard/', FileView.as_view(), name='filemanager_dashboard'),
    path('files_all/', AllFiles.as_view(), name='files_all'),
    path('files_group_view/', FilesGroupView.as_view(), name='files_group_view'),
    path('files_list_view/', FilesListView.as_view(), name='files_list_view'),
    path('starred_files/', StarredFiles.as_view(), name='starred_files'),
    path('shared_files/', SharedFiles.as_view(), name='shared_files'),
    path('shared_outgoing/', SharedOutgoing.as_view(), name='shared_outgoing'),
    path('shared_links/', SharedLinks.as_view(), name='shared_links'),
    path('recover_files/', RecoverFiles.as_view(), name='recover_files'),
    path('file_settings/', FileSettings.as_view(), name='file_settings'),
    path('mailbox/', MailBox.as_view(), name='mailbox'),
    path('messages/', Messages.as_view(), name='messages'),
    path('chats/', Chats.as_view(), name='chats'),
    path('calendar/', Calendar.as_view(), name='calendar'),



	



    
    ]