<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>

<%block name="head">
<style type="text/css">
.dataTables_filter {display: none;}
</style>
</%block>

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
<p>
  The changes listed below include value corrections and additions of new values for existing features.
  Details about specific corrections can be found
  ${h.external_link("https://github.com/clld/wals3/issues?labels=data&milestone=1&state=closed", label='here')}.
</p>
<%util:table items="${changes2013}" eid="t2013" args="item" class_="table-nonfluid">\
    <%def name="head()">
        <th> </th><th>Feature</th><th>Number of added/changed datapoints</th>
    </%def>
    <% vss = list(item[1]) %>
    <td>
      <button title="click to toggle display of datapoints"
              type="button" class="btn btn-mini expand-collapse" data-toggle="collapse" data-target="#c2013-${item[0].pk}">
        <i class="icon icon-plus"> </i>
      </button>
    </td>
    <td>
      ${h.link(request, item[0])}
        <div id="c2013-${item[0].pk}" class="collapse">
          ${util.stacked_links(vss)}
        </div>
    </td>
    <td>${str(len(vss))}</td>
</%util:table>


<h4 id="e2011">WALS Online 2011</h4>

<h5>Value assignment changes</h5>
<p>
  The changes listed below include value corrections and additions of new values for existing features.
</p>
<%util:table items="${changes2011}" eid="t2011" args="item" class_="table-nonfluid">\
    <%def name="head()">
        <th> </th><th>Feature</th><th>Number of added/changed datapoints</th>
    </%def>
    <% vss = list(item[1]) %>
    <td>
      <button title="click to toggle display of datapoints"
              type="button" class="btn btn-mini expand-collapse" data-toggle="collapse" data-target="#c2011-${item[0].pk}">
        <i class="icon icon-plus"> </i>
      </button>
    </td>
    <td>
      ${h.link(request, item[0])}
        <div id="c2011-${item[0].pk}" class="collapse">
          ${util.stacked_links(vss)}
        </div>
    </td>
    <td>${str(len(vss))}</td>
</%util:table>

<h5>Other changes</h5>
<ul>
  <li>
    There are two new chapters (chapter 143 on Order of Negative Morpheme and Verb, and
    chapter 144 on Position of Negative Word With Respect to Subject, Object, and Verb,
    both with many new maps)
  </li>
  <li>
    Additional features have been added to some chapters.
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

<script>
$(document).ready(function() {
    $('.expand-collapse').click(function(){ //you can give id or class name here for $('button')
        $(this).children('i').toggleClass('icon-minus icon-plus');
    });
});
</script>
