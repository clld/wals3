<%inherit file="app.mako"/>

##
## define app-level blocks:
##

<%block name="title">${_('Home')}</%block>
<%block name="header">
<div id="header">
    <a href="${request.resource_url(request.dataset)}">
        <img src="${request.static_url('wals3:static/header.gif')}"/>
    </a>
</div>
</%block>

${next.body()}
