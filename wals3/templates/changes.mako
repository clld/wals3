<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>


<ul class="nav nav-pills pull-right">
  <li class="active">
    <a href="#e2013">2013</a>
  </li>
  <li class="active">
    <a href="#e2011">2011</a>
  </li>
  <li class="active">
    <a href="#e2008">2008</a>
  </li>
</ul>

##http://blog.wals.info/category/errata/

<h4 id="e2013">WALS Online 2013</h4>

<h5>Value assignment changes</h5>

<div class="accordion" id="sidebar-accordion">
% for parameter, vss in changes2013:
    <%util:accordion_group eid="acc-2013-${parameter.id}" parent="sidebar-accordion" title="${parameter.id} ${parameter.name}">
        ${util.stacked_links(sorted(vss, key=lambda vs: vs.language.name))}
    </%util:accordion_group>
% endfor
</div>

<h4 id="e2011">WALS Online 2011</h4>

<h5>Value assignment changes</h5>
<div class="accordion" id="accordion-2011">
% for parameter, vss in changes2011:
    <%util:accordion_group eid="acc-2011-${parameter.id}" parent="accordion-2011" title="${parameter.id} ${parameter.name}">
        ${util.stacked_links(sorted(vss, key=lambda vs: vs.language.name))}
    </%util:accordion_group>
% endfor
</div>

<h5>Other changes</h5>
<ul>
  <li>
    There are two new chapters (chapter 143 on Order of Negative Morpheme and Verb, and
    chapter 144 on Position of Negative Word With Respect to Subject, Object, and Verb,
    both with many new maps)
  </li>
  <li>
    New data for some chapters has been added.
  </li>
  <li>
    Additional maps have been added to chapters 81 (Order of Subject, Object and Verb) and 90 (Order of Relative Clause and Noun).
  </li>
  <li>
    The genealogical classification of languages, including genera, has been updated.
  </li>
  <li>
    The one-to-many relationship between chapters and features/maps is now clearly reflected
    in the structure of WALS: A single chapter can contain not just one feature, but several
    features, most often two (e.g. feature 39A and feature 39B), but sometimes (with the new
    chapters 143 and 144) quite a few features and maps.
  </li>
  <li>
    For some of the features, WALS now includes examples supplied by the authors (for example feature 113A)
  </li>
  <li>
    WALS Online now contains the long introduction chapter of the printed atlas from 2005
  </li>
</ul>

<h4 id="e2008">WALS Online 2008</h4>

<p>
  A description of errate in the printed version of 2005 can be found at
  ${h.external_link('http://blog.wals.info/category/errata/errata-2005/')}.
</p>
