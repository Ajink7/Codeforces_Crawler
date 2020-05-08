from django.views import generic
import datetime
class IndexView(generic.TemplateView):
    # print(datetime.datetime.now())
    template_name = 'index.html'
