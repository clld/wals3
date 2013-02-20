<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>


<h2>${_('Chapter')} ${ctx.name}</h2>

${u.get_description(request, ctx)|n}

<%def name="sidebar()">
<div class="well well-small">
    <h3>Features</h3>
</div>

<div class="well well-small">
    <h3>References</h3>

</div>
</%def>
