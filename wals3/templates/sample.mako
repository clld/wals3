<%inherit file="${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="util.mako"/>
<%namespace name="lib" file="lib.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">Languages</%block>

${lib.languages_contextnav()}

<h2>${ctx.name}</h2>

${req.map.render()}

##${ctx.render()}

<%util:table items="${ctx.languages}" args="item">\
    <%def name="head()">
        <th>&nbsp;</th><th>Code</th><th>Name</th><th>Genus</th><th>Family</th>
    </%def>
    <td>${h.link_to_map(item)}</td>
    <td>${h.link(request, item, label=item.id)}</td>
    <td>${h.link(request, item)}</td>
    <td>${h.map_marker_img(request, item.genus)} ${item.genus.name}</td>
    <td>${h.link(request, item.genus.family)}</td>
</%util:table>
