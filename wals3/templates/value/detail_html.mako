<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>

<%def name="contextnav()">
<li>${h.HTML.a('cite', onclick=h.JSModal.show(ctx.parameter.name, request.resource_url(ctx.parameter.chapter, ext='md.html')))}</li>
</%def>

<h2>${_('Datapoint')} ${ctx.domainelement.name}</h2>

<dl>
    % for attr in ['parameter', 'language', 'contribution']:
    <dt>${attr.capitalize()}:</dt>
    <dd>
        ${h.link(request, getattr(ctx, attr))}
        % if attr == 'contribution':
        by ${h.linked_contributors(request, getattr(ctx, attr))}
        % endif
    </dd>
    % endfor
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

<% history = ctx.history() %>
% if history:
<h3>History</h3>
<ul>
    % for v in history:
    <li>
        ${v.updated} ${h.models.DomainElement.get(v.domainelement_pk).name}
    </li>
    % endfor
</ul>
% endif

<%def name="sidebar()">
  <div class="well well-small">
    <div class="btn-group pull-right">
        <button class="btn">Comment</button>
    </div>
    <div id="comments">
    </div>
  </div>
  <script>
$(document).ready(function() {
  ${h.JSFeed.init(dict(eid="comments", url="http://blog.wals.info/datapoint-"+ctx.parameter.id.lower()+"-wals_code_"+ctx.language.id+"/feed/", title="Comments"))|n}
});
  </script>
</%def>
