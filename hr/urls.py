from django.urls import path
from . import views
from .views import (
    DashboardTemplateView,
    LocationsListView,
    JobTitlesListView,
    JobTitleCreateView,
    JobTitleDetailView,
    JobTitleUpdateView,
    JobTitleDeleteView,
    PayGradeListView,
    PayGradeCreateView,
    PayGradeDetailView,
    PayGradeUpdateView,
    PayGradeDeleteView,
    StaffProfileListView,
    StaffProfileDetailView,

    
)


app_name = 'hr'

urlpatterns = [
	path('dashboard/', DashboardTemplateView.as_view(), name='hr_dashboard'),
    path('locations_list/', LocationsListView.as_view(), name='locations_list'),
    path('job_titles_list/', JobTitlesListView.as_view(), name='job_titles_list'),
    path('add_job_title/', JobTitleCreateView.as_view(), name='add_job_title'),
    path('<uuid:pk>/job_title_detail/', JobTitleDetailView.as_view(), name='job_title_detail'),
    path('<uuid:pk>/job_title_update/', JobTitleUpdateView.as_view(), name='job_title_update'),
    path('<uuid:id>/job_title_delete/', JobTitleDeleteView.as_view(), name='job_title_delete'),
    path('pay_grade_list/', PayGradeListView.as_view(), name='pay_grade_list'),
    path('add_pay_grade/', PayGradeCreateView.as_view(), name='add_pay_grade'),
    path('<uuid:pk>/pay_grade_detail/', PayGradeDetailView.as_view(), name='pay_grade_detail'),
    path('<uuid:pk>/pay_grade_update/', PayGradeUpdateView.as_view(), name='pay_grade_update'),
    path('<uuid:id>/pay_grade_delete/', PayGradeDeleteView.as_view(), name='pay_grade_delete'),
    path('staff_profile_list/', StaffProfileListView.as_view(), name='staff_profile_list'),
    path('<uuid:pk>/staff_profile_detail/', StaffProfileDetailView.as_view(), name='staff_profile_detail'),
    
    
    
    
	
    
    ]