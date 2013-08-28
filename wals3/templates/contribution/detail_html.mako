<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "dataset" %>


<h2>${_('Chapter')} ${ctx.name}</h2>

${text|n}

<%def name="sidebar()">
    % if ctx.features:
    <%util:well title="Features">
        ${util.stacked_links(ctx.features)}
    </%util:well>
    % endif
    <%util:feed title="Comments" url="${request.blog.feed_url(ctx, request)}">
        No comments have been posted.
    </%util:feed>
    <%util:well title="References">
        ${util.stacked_links([ref.source for ref in ctx.references])}
    </%util:well>
</%def>
