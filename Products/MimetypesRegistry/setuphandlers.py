"""
MimetypesRegistry setup handlers.
"""

from zope.component import getUtility

from Products.MimetypesRegistry.interfaces import IMimetypesRegistryTool

from StringIO import StringIO

def fixUpSMIGlobs(out):
    from Products.MimetypesRegistry.mime_types import smi_mimetypes
    from Products.Archetypes.debug import log
    mtr = getUtility(IMimetypesRegistryTool)
    smi_mimetypes.initialize(mtr)

    # Now comes the fun part. For every glob, lookup a extension
    # matching the glob and unregister it.
    for glob in mtr.globs.keys():
        if mtr.extensions.has_key(glob):
            log('Found glob %s in extensions registry, removing.' % glob)
            mti = mtr.extensions[glob]
            del mtr.extensions[glob]
            if glob in mti.extensions:
                log('Found glob %s in mimetype %s extensions, '
                    'removing.' % (glob, mti))
                exts = list(mti.extensions)
                exts.remove(glob)
                mti.extensions = tuple(exts)
                mtr.register(mti)


def installMimetypesRegistry(portal):
    out = StringIO()

    fixUpSMIGlobs(out)


def setupMimetypesRegistry(context):
    """
    Setup MimetypesRegistry step.
    """
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('mimetypes-registry-various.txt') is None:
        return
    out = []
    site = context.getSite()
    installMimetypesRegistry(site)

