<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<h2>${_('Datapoint')} ${h.link(request, ctx.language)} / ${h.link(request, ctx.parameter)}</h2>

<div class="btn-group">
    ${h.button('cite', onclick=h.JSModal.show(ctx.parameter.name, request.resource_url(ctx.parameter.chapter, ext='md.html')))}
    <button class="btn">Comment</button>
</div>

<dl>
    <dt>Language:</dt>
    <dd>${h.link(request, ctx.language)}</dd>
    <dt>Feature:</dt>
    <dd>${h.link(request, ctx.parameter)} by ${h.linked_contributors(request, ctx.contribution)}</dd>
    <dt>Value:</dt>
    <dd>${ctx.values[0].domainelement.name}</dd>
</dl>

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
    <% value = ctx.values[0] %>
    <div class="well well-small">
        <div id="comments">
            No comments have been posted.
        </div>
    </div>
    <script>
$(document).ready(function() {
  ${h.JSFeed.init(dict(eid="comments", url="http://blog.wals.info/datapoint-"+ctx.parameter.id.lower()+"-wals_code_"+ctx.language.id+"/feed/", title="Comments"))|n}
});
    </script>
    <%util:history obj_="${value}" args="item">
        ${h.models.DomainElement.get(item.domainelement_pk).name}
    </%util:history>
    ##<div class="well well-small">
    ##    <h3>History</h3>
    ##    <p>Current version from ${str(value.updated).split('.')[0]}.</p>
    ##    <ul>
    ##        % for v in value.history():
    ##        <li>
    ##            ${str(v.updated).split('.')[0]} ${h.models.DomainElement.get(v.domainelement_pk).name}
    ##        </li>
    ##        % endfor
    ##    </ul>
    ##</div>
</%def>
