from django.shortcuts import render
from django.views.generic import (
     CreateView,
     DetailView,
     ListView,
     UpdateView,
     DeleteView,
     TemplateView
)



from django.db import transaction
from django.db.models import F
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views import static
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
)
from django.views.generic.detail import (
    SingleObjectMixin,
    SingleObjectTemplateResponseMixin,
)
from django.views.generic.edit import FormMixin, ProcessFormView

from .compat import LoginRequiredMixin
from .conf import settings
from .forms import (
    ColleagueFolderShareForm,
    DocumentCreateForm,
    DocumentCreateFormWithName,
    FolderCreateForm,
)
from .hooks import hookset
from .models import Document, Folder, UserStorage
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

class IndexView(LoginRequiredMixin, TemplateView):

    template_name = "administration/index.html"

    def get_context_data(self, **kwargs):
        ctx = kwargs
        ctx.update({
            "members": Folder.objects.members(None, user=self.request.user),
            "storage": self.request.user.storage,
            "can_share": False,
        })
        return ctx


class DashboardView(TemplateView):
    template_name = "administration/admin_dept_dashboard_main.html"

    
    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        return context


class FileView(TemplateView):
    template_name = "administration/admin_filemanager.html"

    
    def get_context_data(self, *args, **kwargs):
        context = super(FileView, self).get_context_data(*args, **kwargs)
        return context

class AllFiles(TemplateView):
    template_name = "administration/admin_files.html"

    
    def get_context_data(self, *args, **kwargs):
        context = super(AllFiles, self).get_context_data(*args, **kwargs)
        return context


class FilesGroupView(TemplateView):
    template_name = "administration/files_group_view.html"

    
    def get_context_data(self, *args, **kwargs):
        context = super(FilesGroupView, self).get_context_data(*args, **kwargs)
        return context
 
class FilesListView(TemplateView):
    template_name = "administration/files_list_view.html"

    
    def get_context_data(self, *args, **kwargs):
        context = super(FilesListView, self).get_context_data(*args, **kwargs)
        return context


class StarredFiles(TemplateView):
    template_name = "administration/starred_files.html"

    
    def get_context_data(self, *args, **kwargs):
        context = super(StarredFiles, self).get_context_data(*args, **kwargs)
        return context


class SharedFiles(TemplateView):
    template_name = "administration/shared_files.html"

    
    def get_context_data(self, *args, **kwargs):
        context = super(SharedFiles, self).get_context_data(*args, **kwargs)
        return context



class SharedOutgoing(TemplateView):
    template_name = "administration/shared_outgoing.html"

    
    def get_context_data(self, *args, **kwargs):
        context = super(SharedOutgoing, self).get_context_data(*args, **kwargs)


class SharedLinks(TemplateView):
    template_name = "administration/shared_links.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SharedLinks, self).get_context_data(*args, **kwargs)

class RecoverFiles(TemplateView):
    template_name = "administration/recovery.html"

    def get_context_data(self, *args, **kwargs):
        context = super(RecoverFiles, self).get_context_data(*args, **kwargs)



class FileSettings(TemplateView):
    template_name = "administration/setting.html"

    def get_context_data(self, *args, **kwargs):
        context = super(FileSettings, self).get_context_data(*args, **kwargs)



class MailBox(TemplateView):
    template_name = "administration/mailbox.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MailBox, self).get_context_data(*args, **kwargs)



class Messages(TemplateView):
    template_name = "administration/messages.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Messages, self).get_context_data(*args, **kwargs)



class Chats(TemplateView):
    template_name = "administration/chats.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Chats, self).get_context_data(*args, **kwargs)


class Calendar(TemplateView):
    template_name = "administration/calendar.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Calendar, self).get_context_data(*args, **kwargs)
