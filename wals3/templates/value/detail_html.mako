<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>


<h2>${_('Datapoint')} ${h.link(request, ctx.valueset.language)} / ${h.link(request, ctx.valueset.parameter)}</h2>

<div class="btn-group">
    ${h.button('cite', onclick=h.JSModal.show(ctx.valueset.parameter.name, request.resource_url(ctx.valueset.parameter.chapter, ext='md.html')))}
    <button class="btn">Comment</button>
</div>

<dl>
    <dt>Language:</dt>
    <dd>${h.link(request, ctx.valueset.language)}</dd>
    <dt>Feature:</dt>
    <dd>${h.link(request, ctx.valueset.parameter)} by ${h.linked_contributors(request, ctx.valueset.contribution)}</dd>
    <dt>Value:</dt>
    <dd>${ctx.domainelement.name}</dd>
</dl>

% if ctx.valueset.references:
<h3>References</h3>
<ul>
    % for ref in ctx.valueset.references:
    <li>
        ${h.link(request, ref.source)}
    </li>
    % endfor
</ul>
% endif

<%def name="sidebar()">
    <div class="well well-small">
        <div id="comments">
            No comments have been posted.
        </div>
    </div>
    <script>
$(document).ready(function() {
  ${h.JSFeed.init(dict(eid="comments", url="http://blog.wals.info/datapoint-"+ctx.valueset.parameter.id.lower()+"-wals_code_"+ctx.valueset.language.id+"/feed/", title="Comments"))|n}
});
    </script>
</%def>
