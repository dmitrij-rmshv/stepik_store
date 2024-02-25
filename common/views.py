from django.views.generic import TemplateView


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class AboutView(TitleMixin, TemplateView):
    template_name = 'products/about.html'
    title = 'O caйте'
