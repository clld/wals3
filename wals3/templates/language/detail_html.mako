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

<div>
    <% dt = request.registry.getUtility(h.interfaces.IDataTable, 'values'); dt = dt(request, h.models.Value, language=ctx) %>
    ${dt.render()}
</div>

<%def name="sidebar()">
    <div class="accordion" id="sidebar-accordion">
        % if request.map:
        <%util:accordion_group eid="acc-map" parent="sidebar-accordion" title="Map" open="${True}">
            ${request.map.render()}
            <p>Coordinates: ${ctx.latitude}, ${ctx.longitude}</p>
            <p>Spoken in: ${', '.join(h.link(request, c) for c in [a.country for a in ctx.country_assocs])|n}</p>
        </%util:accordion_group>
        % endif
        % if ctx.sources:
        <%util:accordion_group eid="sources" parent="sidebar-accordion" title="Sources">
            <ul>
                % for source in ctx.sources:
                <li>${h.link(request, source, label=source.description)}<br />
                <small>${h.link(request, source)}</small></li>
                % endfor
            </ul>
        </%util:accordion_group>
        % endif
        <%util:accordion_group eid="acc-names" parent="sidebar-accordion" title="Alternative names">
            <ul>
                % for identifier in ctx.identifiers:
                <li>${identifier.type} ${identifier.id or identifier.name}</li>
                % endfor
            </ul>
        </%util:accordion_group>
    </div>
</%def>
