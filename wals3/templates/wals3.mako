<%inherit file="app.mako"/>

##
## define app-level blocks:
##

<%block name="head">
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
        google.load("feeds", "1");
    </script>
</%block>

<%block name="header">
<div id="header">
    <a href="${request.resource_url(request.dataset)}">
        <img src="${request.static_url('wals3:static/header.gif')}"/>
    </a>
</div>
</%block>

${next.body()}
