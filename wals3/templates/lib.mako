
<%def name="languages_contextnav()">
    <ul class="nav nav-tabs">
        <li class="${'active' if request.matched_route.name == 'languages' else ''}">
            <a href="${request.route_url('languages')}">Browse</a>
        </li>
        <li class="${'active' if request.matched_route.name == 'genealogy' else ''}">
            <a href="${request.route_url('genealogy')}">Genealogy</a>
        </li>
        <li class="${'active' if request.matched_route.name == 'sample' and request.matchdict['count'] == '100' else ''}">
            <a href="${request.route_url('sample', count='100')}">100-language Sample</a>
        </li>
        <li class="${'active' if request.matched_route.name == 'sample' and request.matchdict['count'] == '200' else ''}">
            <a href="${request.route_url('sample', count='200')}">200-language Sample</a>
        </li>
    </ul>
</%def>
