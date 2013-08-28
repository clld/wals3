<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>


<h2>${_('Datapoint')} ${h.link(request, ctx.language)} / ${h.link(request, ctx.parameter)}</h2>

<dl>
    <dt>Language:</dt>
    <dd>${h.link(request, ctx.language)}</dd>
    <dt>Feature:</dt>
    <dd>${h.link(request, ctx.parameter)} by ${h.linked_contributors(request, ctx.contribution)}</dd>
    <dt>Value:</dt>
    <dd>${ctx.values[0].domainelement.name}</dd>
</dl>

% if ctx.values[0].sentence_assocs:
<h3>Examples</h3>
${util.sentences(ctx.values[0])}
% endif

% if ctx.references:
<h3>References</h3>
<ul>
    % for ref in ctx.references:
    <li>
        ${h.link(request, ref.source)}
    </li>
    % endfor
</ul>
% endif

<%def name="sidebar()">
    <div>
        <form class="inline" method="POST" action="${request.route_url('datapoint', fid=ctx.parameter.id, lid=ctx.language.id)}">
            ${h.button('cite', onclick=h.JSModal.show(ctx.parameter.name, request.resource_url(ctx.parameter.chapter, ext='md.html')))}
            <button type="submit" class="btn">comment</button>
        </form>
    </div>
    <% value = ctx.values[0] %>
    <%util:feed title="Comments" url="${request.blog.feed_url(ctx, request)}">
        No comments have been posted.
    </%util:feed>
    <%util:history obj_="${value}" args="item">
        ${h.models.DomainElement.get(item.domainelement_pk).name}
    </%util:history>
</%def>
