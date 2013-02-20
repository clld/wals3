<%inherit file="${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="util.mako"/>
<%namespace name="lib" file="lib.mako"/>
<%! active_menu_item = "languages" %>

${lib.languages_contextnav()}

<h2>${ctx.name}</h2>

${req.map.render()}

##${ctx.render()}

<table id="languages" class="table table-hover">
    <thead>
        <tr>
            <th>Code</th><th>Name</th>
            <th>Genus</th><th>Family</th>
        </tr>
    </thead>
    <tbody>
        % for language in ctx.languages:
        <tr>
            <td>${h.link(request, language, label=language.id)}</td>
            <td>${h.link(request, language)}</td>
            <td>${language.genus.name}</td>
            <td>${h.link(request, language.genus.family)}</td>
        </tr>
        % endfor
    </tbody>
</table>
<script>
$(document).ready(function() {
    $('#languages').dataTable({bLengthChange: false, bPaginate: false, bInfo: false});
});
</script>
