<%inherit file="wals3.mako"/>
<%! from clld_markdown_plugin import markdown %>
<%namespace name="util" file="util.mako"/>
<%namespace name="lib" file="lib.mako"/>

<%! active_menu_item = "languages" %>
<%block name="title">Genealogy</%block>

<%def name="sidebar()">
    <%util:well>
      ${markdown(req, text)|n}
    </%util:well>
</%def>

${lib.languages_contextnav()}

<h2>Genealogical Language List</h2>
##
## TODO:
## - by Matthew Dryer
## - counts of languages, genera, families
##
<div class="btn-toolbar">
  <div class="btn-group">
    <button onclick="CLLD.TreeView.show(1);" class="btn">Show Genera</button>
    <button onclick="CLLD.TreeView.hide(1);" class="btn">Hide Genera</button>
  </div>
  <div class="btn-group">
    <button onclick="CLLD.TreeView.show(2);" class="btn">Show Languages</button>
    <button onclick="CLLD.TreeView.hide(2);" class="btn">Hide Languages</button>
  </div>
</div>
<div class="treeview">
  <ul>
    % for family in families:
    <li>
      <%util:tree_node_label level="1" id="f-${family.id}" checked="${False}">
        ${h.link(request, family)}
      </%util:tree_node_label>
      <ul>
        % for genus in family.genera:
        <li>
          <%util:tree_node_label level="2" id="g-${genus.id}">
            ${h.link(request, genus)}${' (subfamily: '+genus.subfamily+')' if genus.subfamily else ''}
          </%util:tree_node_label>
          <ul>
            % for language in genus.languages:
            <li>${h.link(request, language)}</li>
            % endfor
          </ul>
        </li>
        % endfor
      </ul>
    </li>
    % endfor
  </ul>
</div>
<script>
$(document).ready(function() {
  CLLD.TreeView.init();
});
</script>
