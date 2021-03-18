<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributors" %>
<%block name="title">${_('Contributor')} ${ctx.name}</%block>

<h2>${ctx.name}</h2>


<dl>
    % if ctx.address:
    <dt>${_('Address')}:</dt>
    <dd>
        <address>
            ${h.text2html(ctx.address)|n}
        </address>
    </dd>
    % endif
    % if ctx.url:
    <dt>${_('Web:')}</dt>
    <dd>${h.external_link(ctx.url)}</dd>
    % endif
    % if ctx.email:
    <dt>${_('Mail:')}</dt>
    <dd>${ctx.email.replace('@', '[at]')}</dd>
    % endif
    ${util.data(ctx, with_dl=False)}
</dl>

<h3>${_('Contributions')}</h3>
<ul>
    % for c in ctx.contribution_assocs:
    <li>${h.link(request, c.contribution)}</li>
    % endfor
</ul>
