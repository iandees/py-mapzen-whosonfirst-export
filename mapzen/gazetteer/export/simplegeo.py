import mapzen.gazetteer.export
import woe.isthat
import logging

class exporter (mapzen.gazetteer.export.flatfile):

    def __init__(self, root, **kwargs):

        mapzen.gazetteer.export.flatfile.__init__(self, root)
        
        self.lookup = None

        if kwargs.get('concordances', None):
            self.lookup = woe.isthat.lookup(kwargs['concordances'])

    def massage_feature(self, f):

        sgid = f.get('id', None)

        props = f['properties']
        props['mz:placetype'] = 'venue'
        props['mz:datasource'] = 'simplegeo'

        props['sg:id'] = sgid

        if self.lookup:

            mzid = self.lookup.woe_id(sgid)

            logging.debug("got %s for %s" % (mzid, sgid))
            
            if mzid != 0:
                props['mz:id'] = mzid

        f['properties'] = props
