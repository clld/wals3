<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>

<%! from sqlalchemy.orm import joinedload %>
<%! from wals3.models import Genus %>

<h2>${_('Family')} ${ctx.name}</h2>

${request.map.render()}

<%def name="sidebar()">
<div class="well well-small">
    <h3>Genera</h3>
    <ul class="nav nav-tabs nav-stacked">
    % for genus in h.DBSession.query(Genus).filter(Genus.family_pk == ctx.pk).options(joinedload(Genus.languages)):
        <li class="dropdown">
            <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                ${genus.name}
                <b class="caret"></b>
            </a>
            <ul class="dropdown-menu">
            % for language in genus.languages:
                <li>${h.link(request, language)}</li>
            % endfor
            </ul>
        </li>
    % endfor
    </ul>
</div>
</%def>
