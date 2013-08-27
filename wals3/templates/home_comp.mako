<%inherit file="${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="util.mako"/>
<%! active_menu_item = "dataset" %>

<%def name="contextnav()">
    ${util.contextnavitem('legal')}
    % if list(request.registry.getUtilitiesFor(h.interfaces.IDownload)):
    ${util.contextnavitem('download')}
    % endif
    ${util.contextnavitem('changes')}
    ${util.contextnavitem('contact')}
</%def>
${next.body()}
