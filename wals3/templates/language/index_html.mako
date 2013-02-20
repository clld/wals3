<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%namespace name="lib" file="../lib.mako"/>
<%! active_menu_item = "languages" %>

${lib.languages_contextnav()}

<h2>${_('Languages')}</h2>

${ctx.render()}
