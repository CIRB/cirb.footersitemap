from plone.app.layout.viewlets.common import FooterViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class FooterSitemapViewlet(FooterViewlet):
    index = ViewPageTemplateFile('templates/footersitemap.pt')
    def get_site_map(self):
	return 'get_site_map'
