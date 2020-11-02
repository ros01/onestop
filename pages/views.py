from django.shortcuts import render
from django.db.models import Q
from django.views.generic import TemplateView, ListView


#def index(request):
    #return render(request, 'pages/index.html')

class HomepageTemplateView(TemplateView):
    template_name = "pages/index.html"
    
    #def get_context_data(self, *args, **kwargs):
        #context = super(HomepageTemplateView, self).get_context_data(*args, **kwargs)
        #context["inspection"] = Schedule.objects.all()
        #return context
