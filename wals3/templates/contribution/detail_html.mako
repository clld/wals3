<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "dataset" %>


<h2>${_('Chapter')} ${ctx.name}</h2>

${u.get_description(request, ctx)|n}

<%def name="sidebar()">
    <%util:well title="Features">
        ${util.stacked_links(ctx.features)}
    </%util:well>
    <%util:well title="References">
        ${util.stacked_links(ctx.references)}
    </%util:well>
</%def>
