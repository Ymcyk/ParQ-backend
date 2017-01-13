from django.shortcuts import render
from django.views import View

class Index(View):
    def get(self, request):
        context = {
                'title': 'ParQ',
                }
        return render(request, 'pages/index.html', context)

