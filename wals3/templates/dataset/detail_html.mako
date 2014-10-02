<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

<%def name="sidebar()">
  <div id="wals_search">
  <script>
  (function() {
    var cx = '012093784907070887713:a7i_0y3rwgs';
    var gcse = document.createElement('script');
    gcse.type = 'text/javascript';
    gcse.async = true;
    gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') +
        '//www.google.com/cse/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(gcse, s);
  })();
  </script>
  <gcse:search></gcse:search>
  </div>
  ${util.feed('WALS News', request.blog.feed_url('category/news', request), eid='news', numEntries=1)}
  ${util.feed('Latest Comments', request.blog.feed_url('comments', request), eid='comments')}
</%def>

<h2>Welcome to WALS Online</h2>

<p class="lead">
    The World Atlas of Language Structures (WALS) is a large database of structural
    (phonological, grammatical, lexical) properties of languages gathered from descriptive
    materials (such as reference grammars) by a team of
    <a href="${request.route_url('contributors')}">${stats['contributor']} authors</a>.
</p>
<p>
    The first version of WALS was published as a book with CD-ROM in 2005 by
    ${h.external_link('http://ukcatalogue.oup.com/product/9780199255917.do', label='Oxford University Press')}.
    The first online version was published in April 2008.
    The second online version was published in April 2011.
</p>
<p>
  The 2013 edition of WALS corrects a number of coding errors expecially in Chapters 1 and 3.
  A full list of changes is available <a href="${request.route_url('changes')}">here</a>.
</p>
<p>
  Starting with this edition of WALS, there will not be specific editions every two or three years, but we will be
  updating it whenever corrections or additions are made. Changes in value assignment will be made transparent by
  showing a history on the respective pages.
</p>
<p>
    WALS Online is a publication of the
    ${h.external_link('http://www.eva.mpg.de', label='Max Planck Institute for Evolutionary Anthropology')}.
    It is a separate publication, edited by
    Dryer, Matthew S. & Haspelmath, Martin (Leipzig: Max Planck Institute for Evolutionary Anthropology, 2013)
    The main programmer is Robert Forkel.
</p>

<h3>How to use WALS Online</h3>
<p>
    Using WALS Online requires a browser with Javascript enabled.
</p>
<p>
    You find the features or chapters of WALS through the items "Features" and "Chapters"
    in the navigation bar.
</p>
<p>
  You can also browse and search for languages through the item "Languages" on the navigation bar.
</p>
<p>
    You can search for references through the item "References", and once you have
    navigated to a particular feature, you see a second navigation bar with citation
    information and various export options.
</p>
<p>
  A description of changes from previous editions is available through the item
  "Changes".
</p>

<h3>How to cite WALS Online</h3>
<p>
  It is important to cite the specific chapter that you are taking your information from,
  not just the general work
  "The World Atlas of Language Structures Online" (Dryer, Matthew S. & Haspelmath, Martin 2013),
  unless you are citing data from more than 25 chapters simultaneously.
</p>
<p>
  We recommend that you cite
</p>
  <ul class="unstyled">
    <li>
    the general work as ${h.cite_button(request, ctx)}
<blockquote>
    ${h.newline2br(citation.render(ctx, request))|n}
</blockquote>
    </li>
    <li>
    and WALS Online chapters as in the following example
<blockquote>
    ${h.newline2br(citation.render(example_contribution, request))|n}
</blockquote>
    </li>

<h3>Interactive Reference Tool (WALS program)</h3>
<p>
    The World Atlas of Language Structures was published as a book with a CD-ROM in summer 2005.
    The CD-ROM contains the "Interactive Reference Tool (WALS program)" as a standalone application
    for Mac OSX, Mac OS9.2 and Windows 2000, XP written by
    ${h.external_link('http://www.eva.mpg.de/lingua/staff/bibiko.php', label=u'Hans-Jörg Bibiko')}.
    To download the
    "Interactive Reference Tool (WALS program)" please follow the link
    ${h.external_link('http://www.eva.mpg.de/lingua/research/tool.php')}.
</p>
<h3>Terms of use</h3>
<p>
    The content of this web site is published under a Creative Commons Licence.
    We invite the community of users to think about further applications for the available data
    and look forward to your comments, feedback and questions.
</p>
