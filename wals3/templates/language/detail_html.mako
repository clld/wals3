<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">Language ${ctx.name}</%block>

<ul class="breadcrumb">
    <li>Family: ${h.link(request, ctx.genus.family)} <span class="divider">/</span></li>
    % if ctx.genus.subfamily:
    <li class="active">Subfamily: ${ctx.genus.subfamily} <span class="divider">/</span></li>
    % endif
    <li class="active">Genus: ${h.link(request, ctx.genus)}</li>
</ul>

<h2>Language ${ctx.name}</h2>

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    ${util.codes()}
    <div style="clear: right;"> </div>
    <%util:well>
        ${request.map.render()}
        ${h.format_coordinates(ctx)}
        ${util.dl_table(('Spoken in', h.literal(', '.join(h.link(request, c) for c in ctx.countries))))}
    </%util:well>
    <%util:well title="Alternative names">
        ${util.dl_table(*[(i.description.capitalize(), i.name) for i in ctx.identifiers if i.type == 'name'])}
    </%util:well>
    % if ctx.sources:
    <%util:well title="Sources">
        ${util.sources_list(sorted(list(ctx.sources), key=lambda s: s.name))}
    </%util:well>
    % endif
    ##    <%util:accordion_group eid="acc-names" parent="sidebar-accordion" title="Alternative names">
    ##        <ul>
    ##            % for identifier in ctx.identifiers:
    ##            <li>${identifier.type} ${identifier.id or identifier.name}</li>
    ##            % endfor
    ##        </ul>
    ##    </%util:accordion_group>
    ##</div>
</%def>
