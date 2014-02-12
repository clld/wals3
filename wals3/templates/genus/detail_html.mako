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

<h3>Languages</h3>
<div id="list-container" class="row-fluid">
    % for languages in h.partitioned(ctx.languages):
    <div class="span4">
        <table class="table table-condensed table-nonfluid">
            <tbody>
                % for language in languages:
                <tr>
                    <td>${h.link_to_map(language)}</td>
                    <td>${h.link(request, language)}</td>
                </tr>
                % endfor
            </tbody>
        </table>
    </div>
    % endfor
</div>
