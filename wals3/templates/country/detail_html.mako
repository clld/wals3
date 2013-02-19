<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>


<h2>${_('Country')} ${ctx.name}</h2>

${request.map.render()}

<%def name="sidebar()">
<div class="well well-small">
    <h3>Languages</h3>
    <ul class="nav nav-tabs nav-stacked">
    % for language in sorted(ctx.languages, key=lambda l: l.name):
        <li>${h.link(request, language)}</li>
    % endfor
    </ul>
</div>
</%def>
