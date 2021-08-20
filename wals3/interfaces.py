from zope.interface import Interface


class IFamily(Interface):

    """marker."""


class IGenus(Interface):

    """marker."""


class ICountry(Interface):

    """marker."""


class IBlog(Interface):

    """utility to integrate a blog."""

    def feed_url(self, ctx, req):
        """return URL of the comment feed for an object (or None)."""

    def post_url(self, ctx, req):
        """return URL of a corresponding post."""

