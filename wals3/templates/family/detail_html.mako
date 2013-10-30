<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">Family ${ctx.name}</%block>

<%! from sqlalchemy.orm import joinedload %>
<%! from wals3.models import Genus %>

<h2>Family ${ctx.name}</h2>

${request.map.render()}

<%def name="sidebar()">
    <%util:well title="Genera">
    <div class="accordion" id="sidebar-accordion">
        % for genus in h.DBSession.query(Genus).filter(Genus.family_pk == ctx.pk).order_by(Genus.name).options(joinedload(Genus.languages)):
        <%util:accordion_group eid="acc-${genus.id}" parent="sidebar-accordion">
            <%def name="title()">
                <img height="20" width="20" src="${u.wals3.map_marker(genus, request)}" />
                ${genus.name} (${len(genus.languages)} language${'s' if len(genus.languages)> 1 else ''})
            </%def>
            <table class="table table-condensed table-nonfluid">
                <tbody>
                    % for language in genus.languages:
                    <tr>
                        <td>${u.link_to_map(language)}</td>
                        <td>${h.link(request, language)}</td>
                    </tr>
                    % endfor
                </tbody>
            </table>
        </%util:accordion_group>
        % endfor
    </div>
    </%util:well>
</%def>
