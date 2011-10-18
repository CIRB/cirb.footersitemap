from plone.app.layout.viewlets.common import FooterViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class FooterSitemapViewlet(FooterViewlet):
    
    def render(self):
	# defer to index method, because that's what gets overridden by the template ZCML attribute
	return self.index()
   
    index = ViewPageTemplateFile('templates/footersitemap.pt')
    
    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')
    
    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()
    
    def get_site_map(self):
	folders=[]
	base_path = '/'.join(self.portal.getPhysicalPath())
	return self.get_three_level_folder(base_path)
    
    
    def get_three_level_folder(self, folder_path):
	results=[]
	folders=self.get_folders(folder_path)
	for folder in folders:
	    folder['content']=self.get_folders('/'.join(folder['physical_path']))
	    for subfolder in folder['content']:
		subfolder['content']=self.get_folders('/'.join(subfolder['physical_path']))
	    results.append(folder)
	return results
    
    def get_folders(self,folder_path):
	folders = self.portal_catalog.searchResults(portal_type='Folder', 
	                                         review_state = "published", 
	                                         path={'query': folder_path, 'depth': 1},
	                                         sort_on='getObjPositionInParent')
	results=[]
	for folder in folders:
	    obj = folder.getObject()
	    results.append({'title':obj.Title(),'url':obj.absolute_url(), 'content':[], 'physical_path':obj.getPhysicalPath()})
	return results