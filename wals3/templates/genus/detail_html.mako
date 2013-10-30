<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">Genus ${ctx.name}</%block>

<ul class="breadcrumb">
    <li>
        Family: ${h.link(request, ctx.family)}
        % if ctx.subfamily:
        <span class="divider">/</span>
        % endif
    </li>
    % if ctx.subfamily:
    <li class="active">Subfamily: ${ctx.subfamily}</li>
    % endif
</ul>

<h2>Genus ${ctx.name}</h2>

${request.map.render()}

<%def name="sidebar()">
    <%util:well title="${str(len(ctx.languages))} language${'s' if len(ctx.languages)> 1 else ''}">
        <table class="table table-condensed">
            <tbody>
                % for language in ctx.languages:
                <tr>
                    <td>${u.link_to_map(language)}</td>
                    <td>${h.link(request, language)}</td>
                </tr>
                % endfor
            </tbody>
        </table>
    </%util:well>
</%def>
