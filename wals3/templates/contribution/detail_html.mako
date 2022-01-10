<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>
<%block name="title">Chapter ${ctx.name}</%block>

<h2>Chapter ${ctx.name}</h2>
<p>
 by ${h.linked_contributors(request, ctx)} ${h.cite_button(request, ctx)}
</p>

${text|n}

<%def name="sidebar()">
    % if ctx.features:
    <%util:well title="Related map(s)">
        ${util.stacked_links(sorted(ctx.features, key=lambda f: f.id))}
    </%util:well>
    % endif
    <%util:well title="References">
        ${util.stacked_links([ref.source for ref in ctx.references])}
    </%util:well>
</%def>
