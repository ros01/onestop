import os
import uuid

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

#from .conf import settings
from django.conf import settings
User = get_user_model()


class DocumentsDefaultHookSet:

    def share_with_options(self, user, folder):
        """
        Return a list of users with whom `user` can share `folder`.
        """
        user_class = get_user_model()
        return user_class.objects.all()

    def can_share_folder(self, user, folder):
        """
        Return True if `user` can share `folder`.
        """
        return folder.parent_id is None and folder.author_id == user.id

    def storage_color(self, user_storage):
        """
        Return labels indicating amount of storage used.
        """
        p = user_storage.percentage
        if p >= 0 and p < 60:
            return "success"
        if p >= 60 and p < 90:
            return "warning"
        if p >= 90 and p <= 100:
            return "danger"
        raise ValueError("percentage out of range")

    def folder_created_message(self, request, folder):
        """
        Send messages.success message after successful folder creation.
        """
        messages.success(request, _(f"Folder {folder} was created"))

    def document_created_message(self, request, document):
        """
        Send messages.success message after successful document creation.
        """
        messages.success(request, _(f"Document {document} was created"))

    def folder_shared_message(self, request, user, folder):
        """
        Send messages.success message after successful share.
        """
        messages.success(request, _(f"Folder {folder} is now shared with {user}"))

    def folder_unshared_message(self, request, user, folder):
        """
        Send messages.success message after successful unshare.
        """
        messages.success(request, _(f"User {user} no longer shares Folder {folder}"))

    def document_deleted_message(self, request, document):
        """
        Send messages.success message after successful document deletion.
        """
        messages.success(request, _("Document has been deleted"))

    def folder_deleted_message(self, request, folder):
        """
        Send messages.success message after successful document deletion.
        """
        messages.success(request, _("Folder has been deleted"))

    def folder_pre_delete(self, request, folder):
        """
        Perform folder operations prior to deletions. For example, deleting all contents.
        """
        for m in folder.members():
            if m.__class__ == folder.__class__:
                self.folder_pre_delete(request, m)
            m.delete()

    def file_upload_to(self, instance, filename):
        """
        Callable passed to the FileField's upload_to kwarg on Document.file
        """
        ext = filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join("document", filename)

    def already_exists_validation_message(self, name, folder):
        return f"{name} already exists."


class HookProxy:

    def __getattr__(self, attr):
        return getattr(settings.DOCUMENTS_HOOKSET, attr)

        #return getattr(settings, 'DOCUMENTS_HOOKSET', 5)

       


hookset = HookProxy()
