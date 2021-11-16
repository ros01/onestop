from django.contrib import admin

from .models import Folder, Document, UserStorage


class FolderAdmin(admin.ModelAdmin):
  list_display = ('name', 'parent', 'author')
  list_display_links = ('name', 'parent', 'author')
  list_filter = ('name', 'parent', 'author')
  search_fields = ('name', 'parent', 'author')
  list_per_page = 25


admin.site.register(Folder, FolderAdmin)



class DocumentAdmin(admin.ModelAdmin):
  list_display = ('name', 'folder')
  list_display_links = ('name', 'folder')
  list_filter = ('name', 'folder')
  search_fields = ('name', 'folder')
  list_per_page = 25


admin.site.register(Document, DocumentAdmin)


class UserStorageAdmin(admin.ModelAdmin):
  list_display = ('user', 'bytes_used', 'bytes_total')
  list_display_links = ('user', 'bytes_used', 'bytes_total')
  list_filter = ('user', 'bytes_used', 'bytes_total')
  search_fields = ('user', 'bytes_used', 'bytes_total')
  list_per_page = 25


admin.site.register(UserStorage, UserStorageAdmin)
