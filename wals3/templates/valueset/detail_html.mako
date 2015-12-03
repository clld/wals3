<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">Datapoint ${ctx.name}</%block>


<h2>Datapoint ${h.link(request, ctx.language)} / ${h.link(request, ctx.parameter)}</h2>

${util.dl_table(('Language', h.link(request, ctx.language)), ('Feature', h.HTML.span(h.link(request, ctx.parameter), ' by ', h.linked_contributors(request, ctx.contribution))), ('Value', ctx.values[0].domainelement.name))}

% if ctx.values[0].sentence_assocs:
<h3>Examples</h3>
${util.sentences(ctx.values[0])}
% endif

% if ctx.references:
<h3>References</h3>
<ul>
    % for ref in ctx.references:
        % if ref.source:
    <li>
        ${h.link(request, ref.source)}
    </li>
        % endif
    % endfor
</ul>
% endif

<%def name="sidebar()">
    <div>
        <form class="inline">
            ${h.button('cite', onclick=h.JSModal.show(ctx.parameter.name, request.resource_url(ctx.parameter.chapter, ext='md.html')))}
        </form>
        ${u.comment_button(request, ctx.parameter, ctx.language)}
    </div>
    <% value = ctx.values[0] %>
    <%util:feed title="Comments" url="${request.route_url('blog_feed', _query=dict(path=request.blog.feed_path(ctx, request)))}">
        No comments have been posted.
    </%util:feed>
    <%util:history obj_="${value}" args="item">
        ${h.models.DomainElement.get(item.domainelement_pk).name}
    </%util:history>
</%def>
