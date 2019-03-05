# -*- coding: utf-8 -*-
from plone.app.layout.viewlets.common import FooterViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.navigation.root import getNavigationRootObject


class FooterSitemapViewlet(FooterViewlet):

    def render(self):
        # defer to index method,
        # because that's what gets overridden by the template ZCML attribute
        return self.index()

    index = ViewPageTemplateFile('templates/footersitemap.pt')

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_footer(self):
        root = getNavigationRootObject(self.context, self.portal)
        #lang = self.context.Language()
        lang = getToolByName(self.context,
                            'portal_languages').getPreferredLanguage()
        #print "Langage : %s" % lang
        doc_ids = ['footer-%s' % lang, 'footer']

        lrf = getattr(root, lang, None)
        if not INavigationRoot.providedBy(lrf):
            lrf = None

        for doc_id in doc_ids:
            if doc_id in root.contentIds():
                return get_document(root, doc_id)
            elif lrf and doc_id in lrf.contentIds():
                return get_document(lrf, doc_id)
        return self.get_site_map()

    def get_site_map(self):
        root = getNavigationRootObject(self.context, self.portal)
        base_path = '/'.join(root.getPhysicalPath())
        three_level_fodler = self.get_three_level_folder(base_path)
        return to_html(three_level_fodler)

    def get_three_level_folder(self, folder_path):
        results = []
        folders = self.get_folders(folder_path)
        for folder in folders:
            folder['content'] = self.get_folders(folder['path'])
            for subfolder in folder['content']:
                subfolder['content'] = self.get_folders(folder['path'])
            results.append(folder)
        return results

    def get_folders(self, folder_path):
        folders = self.portal_catalog.searchResults(
                            portal_type=('Folder', 'Document', 'Link',),
                            path={'query': folder_path, 'depth': 1},
                            sort_on='getObjPositionInParent')
        results = []
        for folder in folders:
            if not folder.exclude_from_nav:
                results.append({'title': folder.Title,
                                'url': folder.getURL(),
                                'id': folder.id,
                                'content': [],
                                'path': folder.getPath()})
        return results


def get_document(root, doc_id):
    try:
        text = root.get(doc_id).getText()
    except Exception:
        text = ""
    return text


def to_html(folders):
    html = '<ul>'
    for folder in folders:
        html += '<li class="footer-column">'
        html += dossier_to_html(folder)
        html += '</li>'
    html += '</ul>'
    return html


def dossier_to_html(folder):
    html = '<a href="%s" class="%s"><p>%s</p></a>' % (folder.get("url"),
                                                      folder.get('id'),
                                                      folder.get("title"))
    if folder.get("content"):
        html += '<ul>'
        for sub_folder in folder.get("content"):
            html += '<li>'
            html += dossier_to_html(sub_folder)
            html += '</li>'
        html += '</ul>'
    return html
