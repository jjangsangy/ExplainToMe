from collections import defaultdict


class HTTPURLEndpoints(defaultdict):
    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return self.__getitem__(key)

    def __setattr__(self, name, value):
        if hasattr(HTTPURLEndpoints, name):
            raise AttributeError()
        else:
            self[name] = value

    def __getitem__(self, name):
        if name not in self:
            self[name] = HTTPURLEndpoints()
        return super(HTTPURLEndpoints, self).__getitem__(name)

    def serialize(self):
        base = {}
        if '_ipython_display_' in self:
            self.pop('_ipython_display_')
        if '_getAttributeNames' in self:
            self.pop('_getAttributeNames')
        if 'trait_names' in self:
            self.pop('trait_names')
        for key, value in self.items():
            if isinstance(value, type(self)):
                base[key] = value.serialize()
            elif isinstance(value, (list, tuple)):
                base[key] = type(value)(item.serialize() if
                                        isinstance(item, type(self)) else item
                                        for item in value)
            else:
                base[key] = value
        return base

    @classmethod
    def build_endpoints(cls):

        webapi = HTTPURLEndpoints()

        webapi.sentiment.url = '/url/URLGetTextSentiment'
        webapi.sentiment.text = '/text/TextGetTextSentiment'
        webapi.sentiment.html = '/html/HTMLGetTextSentiment'
        webapi.sentiment_targeted.url = '/url/URLGetTargetedSentiment'
        webapi.sentiment_targeted.text = '/text/TextGetTargetedSentiment'
        webapi.sentiment_targeted.html = '/html/HTMLGetTargetedSentiment'
        webapi.author.url = '/url/URLGetAuthor'
        webapi.author.html = '/html/HTMLGetAuthor'
        webapi.keywords.url = '/url/URLGetRankedKeywords'
        webapi.keywords.text = '/text/TextGetRankedKeywords'
        webapi.keywords.html = '/html/HTMLGetRankedKeywords'
        webapi.concepts.url = '/url/URLGetRankedConcepts'
        webapi.concepts.text = '/text/TextGetRankedConcepts'
        webapi.concepts.html = '/html/HTMLGetRankedConcepts'
        webapi.entities.url = '/url/URLGetRankedNamedEntities'
        webapi.entities.text = '/text/TextGetRankedNamedEntities'
        webapi.entities.html = '/html/HTMLGetRankedNamedEntities'
        webapi.category.url = '/url/URLGetCategory'
        webapi.category.text = '/text/TextGetCategory'
        webapi.category.html = '/html/HTMLGetCategory'
        webapi.relations.url = '/url/URLGetRelations'
        webapi.relations.text = '/text/TextGetRelations'
        webapi.relations.html = '/html/HTMLGetRelations'
        webapi.language.url = '/url/URLGetLanguage'
        webapi.language.text = '/text/TextGetLanguage'
        webapi.language.html = '/html/HTMLGetLanguage'
        webapi.text.url = '/url/URLGetText'
        webapi.text.html = '/html/HTMLGetText'
        webapi.text_raw.url = '/url/URLGetRawText'
        webapi.text_raw.html = '/html/HTMLGetRawText'
        webapi.title.url = '/url/URLGetTitle'
        webapi.title.html = '/html/HTMLGetTitle'
        webapi.feeds.url = '/url/URLGetFeedLinks'
        webapi.feeds.html = '/html/HTMLGetFeedLinks'
        webapi.microformats.url = '/url/URLGetMicroformatData'
        webapi.microformats.html = '/html/HTMLGetMicroformatData'
        webapi.combined.url = '/url/URLGetCombinedData'
        webapi.combined.text = '/text/TextGetCombinedData'
        webapi.image.url = '/url/URLGetImage'
        webapi.imagetagging.url = '/url/URLGetRankedImageKeywords'
        webapi.imagetagging.image = '/image/ImageGetRankedImageKeywords'
        webapi.facetagging.url = '/url/URLGetRankedImageFaceTags'
        webapi.facetagging.image = '/image/ImageGetRankedImageFaceTags'
        webapi.taxonomy.url = '/url/URLGetRankedTaxonomy'
        webapi.taxonomy.html = '/html/HTMLGetRankedTaxonomy'
        webapi.taxonomy.text = '/text/TextGetRankedTaxonomy'

        return webapi.serialize()
