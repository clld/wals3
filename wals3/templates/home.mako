<%inherit file="wals3.mako"/>

<%def name="sidebar()">
  <div id="wals_news" class="well well-small">
  </div>
  <div id="latest_comments" class="well well-small">
  </div>
  <script>
$(document).ready(function() {
    CLLD.Feed.init(${h.dumps(dict(eid="wals_news", url="http://blog.wals.info/category/news/feed/", title="WALS News"))|n});
    CLLD.Feed.init(${h.dumps(dict(eid="latest_comments", url="http://blog.wals.info/comments/feed/", title="Latest Comments"))|n});
});
  </script>
</%def>

<h2>Welcome to WALS Online</h2>

<p class="lead">
The World Atlas of Language Structures (WALS) is a large database of structural
(phonological, grammatical, lexical) properties of languages gathered from descriptive
materials (such as reference grammars) by a team of 55 authors (many of them the
leading authorities on the subject).
</p>
<p>
  The first version of WALS was published as a book with CD-ROM in 2005 by
  Oxford University Press. The first online version was published in April 2008.
  Both are superseeded by the current online version, published in April 2011.
</p>
<p>
  WALS Online is a joint effort of the Max Planck Institute for Evolutionary Anthropology
  and the Max Planck Digital Library. It is a separate publication, edited by
  Dryer, Matthew S. & Haspelmath, Martin (Munich: Max Planck Digital Library, 2011)
  ISBN: 978-3-9813099-1-1. The main programmer is Robert Forkel.
</p>

##<%def name="below_sidebar()">
##  <div class="section">
##    <h3>section header</h3>
##    <p>
##      paragraph with lots of text. in fact enpugh to fill the space below the sidebar.
##      adasfsaf safafds gdsf fdsf dsfds fdsg f ghfd t bgf hgf hh gfh gfh gf ds fds td t.
##    </p>
##  </div>
##</%def>
