<%inherit file="wals3.mako"/>

<%def name="sidebar()">
  <div id="wals_news" class="well well-small">
  </div>
  <div id="latest_comments" class="well well-small">
  </div>
  <script>
$(document).ready(function() {
  ${h.JSFeed.init(dict(eid="wals_news", url="http://blog.wals.info/category/news/feed/", title="WALS News"))|n};
  ${h.JSFeed.init(dict(eid="latest_comments", url="http://blog.wals.info/comments/feed/", title="Latest Comments"))|n}
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

<h3>How to use WALS Online</h3>
<p>
  Using WALS Online requires a browser (supported by Google Maps) with Javascript enabled.
</p>
<p>
  You find the features or chapters of WALS through the items "Features" and "Chapters"
  in the navigation bar.
</p>
<p>
  You can also browse and search for languages and language families alphabetically, by
  map region or by country through the item "Languages" on the navigation bar.
</p>
<p>
  You can search for references through the item "References", and once you have
  navigated to a particular feature, you see a second navigation bar with citation
  information and various export options.
</p>

<h3>New in WALS Online 2011</h3>
<p>
  WALS Online 2011 has a number of new elements:
<p>
<ul>
  <li>
    There are two new chapters (chapter 143 on Order of Negative Morpheme and Verb, and
    chapter 144 on Position of Negative Word With Respect to Subject, Object, and Verb,
    both with many new maps)
  </li>
  <li>
    New data for some chapters has been added. WALS Online now includes 76492 datapoints for 2678 languages. The feature with the most languages (Order of Object and Verb) now has data for 1519 languages.
  </li>
  <li>
    Additional maps have been added to chapters 81 (Order of Subject, Object and Verb) and 90 (Order of Relative Clause and Noun).
  </li>
  <li>
    The genealogical classification of languages, including genera, has been updated.
  </li>
  <li>
    The one-to-many relationship between chapters and features/maps is now clearly reflected in the structure of WALS: A single chapter can contain not just one feature, but several features, most often two (e.g. feature 39A and feature 39B), but sometimes (with the new chapters 143 and 144) quite a few features and maps.
  </li>
  <li>
    For some of the features, WALS now includes examples supplied by the authors (for example feature 113A)
  </li>
  <li>
    WALS Online now contains the long introduction chapter of the printed atlas from 2005
  </li>
</ul>

<h3>How to cite WALS Online</h3>
<p>
  It is important to cite the specific chapter that you are taking your information from, not just the general work "The World Atlas of Language Structures Online" (Dryer, Matthew S. & Haspelmath, Martin 2011), unless you are citing data from more than 25 chapters simultaneously.
</p>
<p>
  We recommend that you cite
</p>
  <ul class="unstyled">
    <li>
    the general work as
    <pre>
Dryer, Matthew S. & Haspelmath, Martin (eds.). 2011. The World Atlas of Language Structures Online.
Munich: Max Planck Digital Library.
Available online at http://wals.info/
Accessed on 2013-02-17.</pre>
    </li>
    <li>
    and WALS Online chapters as in the following example
    <pre>
Maddieson, Ian. 2011. Consonant Inventories.
In: Dryer, Matthew S. & Haspelmath, Martin (eds.)
The World Atlas of Language Structures Online.
Munich: Max Planck Digital Library, chapter 1.
Available online at http://wals.info/chapter/1
Accessed on 2013-02-17.</pre>
    </li>

<h3>Interactive Reference Tool (WALS program)</h3>
<p>
The World Atlas of Language Structures was published as a book with a CD-ROM in summer 2005. The CD-ROM contains the "Interactive Reference Tool (WALS program)" as a standalone application for Mac OSX, Mac OS9.2 and Windows 2000, XP written by Hans-Jörg Bibiko. To download the "Interactive Reference Tool (WALS program)" please follow the link http://www.eva.mpg.de/lingua/research/tool.php.
Terms of use
</p>
<p>
The content of this web site is published under a Creative Commons Licence. Use of the Google base maps is subject to Google's permission guidelines. We invite the community of users to think about further applications for the available data and look forward to your comments, feedback and questions.
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
