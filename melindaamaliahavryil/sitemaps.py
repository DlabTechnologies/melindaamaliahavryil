from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class Melindaamaliahavryil_Static_Sitemap(Sitemap):

    priority = 1.0
    changefreq = 'yearly'

    def items(self):
        return ['about_page', 'resources_page','home_page']

    def location(self, item):
        return reverse(item)




