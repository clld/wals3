<%inherit file="app.mako"/>

##
## define app-level blocks:
##

<%block name="head">
    ##<link href="${request.static_url('wals3:static/wals3.css')}" rel="stylesheet"/>
    ##<script src="${request.static_url('wals3:static/wals3.js')}"></script>
    <link href="${request.static_url('wals3:static/descriptions/style.css')}" rel="stylesheet"/>
</%block>

##<%block name="header">WALS</%block>

<%block name="header">
    <a href="${request.resource_url(request.dataset)}">
        <img src="${request.static_url('wals3:static/header.gif')}"/>
    </a>
</%block>


<%block name="footer">
    <table style="width: 100%; border-top: 1px solid black;">
        <tr>
            <td style="width: 33%;">published</td>
            <td style="width: 33%; text-align: center;">license</td>
            <td style="width: 33%; text-align: right;">disclaimer</td>
        </tr>
    </table>
</%block>

${next.body()}
