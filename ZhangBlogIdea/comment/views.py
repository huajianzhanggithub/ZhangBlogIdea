from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView

from .forms import CommentForm


# Create your views here.
class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            success = True
            return redirect(target)
        else:
            success = False

        context = {
            'success': success,
            'form': comment_form,
            'target': target,
        }
        return self.render_to_response(context)
