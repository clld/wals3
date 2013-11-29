<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>

<h2>${_('Country')} ${ctx.name}</h2>

${request.map.render()}

<%def name="sidebar()">
<div class="well well-small">
    <h3>Languages</h3>
    <table class="table table-condensed">
	<tbody>
	    % for language in ctx.languages:
            <tr>
		<td>${h.link_to_map(language)}</td>
		<td>${h.link(request, language)}</td>
	    </tr>
	    % endfor
	</tbody>
    </table>
</div>
</%def>
