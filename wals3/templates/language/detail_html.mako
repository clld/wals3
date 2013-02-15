<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>


<ul class="breadcrumb">
    <li>Family: ${h.link(request, ctx.genus.family)} <span class="divider">/</span></li>
    % if ctx.genus.subfamily:
    <li class="active">Subfamily: ${ctx.genus.subfamily} <span class="divider">/</span></li>
    % endif
    <li class="active">Genus: ${ctx.genus.name}</li>
</ul>

<h2>${_('Language')} ${ctx.name}</h2>

<ul>
% for identifier in ctx.identifiers:
<li>${identifier.id}</li>
% endfor
</ul>

<div>
    <% dt = request.registry.getUtility(h.interfaces.IDataTable, 'values'); dt = dt(request, h.models.Value, language=ctx) %>
    ${dt.render()}
</div>

<%def name="sidebar()">
    % if request.map:
    ${request.map.render()}
    % endif
    <div class="well well-small">
        <h3>Sources</h3>
        <ul>
            % for source in ctx.sources:
            <li>${h.link(request, source, label=source.description)}<br />
            <small>${h.link(request, source)}</small></li>
            % endfor
        </ul>
    </div>
</%def>
