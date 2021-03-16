<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributors" %>
<%block name="title">${_('Contributors')}</%block>

<h2>${_('Contributors')}</h2>
<div>
    ${ctx.render()}
</div>
