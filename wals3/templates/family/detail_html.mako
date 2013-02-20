<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>

<%! from sqlalchemy.orm import joinedload %>
<%! from wals3.models import Genus %>

<h2>${_('Family')} ${ctx.name}</h2>

${request.map.render()}

<%def name="sidebar()">
<div class="well well-small">
    <h3>Genera</h3>
    <ul class="nav nav-tabs nav-stacked">
    % for genus in h.DBSession.query(Genus).filter(Genus.family_pk == ctx.pk).order_by(Genus.name).options(joinedload(Genus.languages)):
        <li class="dropdown">
            <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                <img src="${request.static_url('wals3:static/icons/%s.png' % genus.icon_id)}" />
                ${genus.name}
                <b class="caret"></b>
            </a>
            <ul class="dropdown-menu">
                <li onclick='CLLD.Map.toggleLayer(${h.dumps(genus.name)}, this.firstElementChild.firstElementChild);'>
		    <label class="checkbox inline" style="margin-left: 5px; margin-right: 5px;">
			<input type="checkbox" checked="checked" />
                        toggle map markers
                    </label>
                </li>
                <li class="divider"></li>
                % for language in genus.languages:
                    <li>${h.link(request, language)}</li>
                % endfor
            </ul>
        </li>
    % endfor
    </ul>
</div>
</%def>
