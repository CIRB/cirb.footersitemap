from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class CirbFootersitemap(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import cirb.footersitemap
        xmlconfig.file('configure.zcml',
                       cirb.footersitemap,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        pass

CIRB_FOOTERSITEMAP_FIXTURE = CirbFootersitemap()
CIRB_FOOTERSITEMAP_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(CIRB_FOOTERSITEMAP_FIXTURE, ),
                       name="CirbFootersitemap:Integration")