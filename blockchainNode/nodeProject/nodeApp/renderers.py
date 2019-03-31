from rest_framework.renderers import BrowsableAPIRenderer
from nodeProject.nodeApp import urls
from django.urls import resolve

class BrowsableAPIExtendedRenderer(BrowsableAPIRenderer):

    def get_breadcrumbs(self, request):
        breadcrumbs_list = []

        for url in urls.urlpatterns:
            pattern = "/" + str(url.pattern)
            try:
                (view, unused_args, unused_kwargs) = resolve(pattern)
                cls = getattr(view, 'cls', None)
                initkwargs = getattr(view, 'initkwargs', {})
                c = cls(**initkwargs)
                name = c.get_view_name()

                #breadcrumbs_list.insert(0, (name, pattern))
                breadcrumbs_list.append((name, pattern))
            except Exception:
                pass

        return breadcrumbs_list