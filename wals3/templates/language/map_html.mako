<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">Selected Languages</%block>

<%! from sqlalchemy.orm import joinedload %>
<%! from wals3.models import Genus %>

<ul class="nav nav-pills pull-right">
    <li><a href="#map-container">Map</a></li>
    <li><a href="#list-container">Genera</a></li>
</ul>

<h2>Selected Languages</h2>

${util.dl_table(*ctx.filters)}

${map.render()}

<div id="list-container" class="row-fluid">
    % for langs in h.partitioned(languages, n=4):
    <div class="span3">
        <table class="table table-condensed table-nonfluid">
            <tbody>
                % for language in langs:
                <tr>
                    <td><img title="genus: ${language.genus.name}" height="20" width="20" src="${u.wals3.map_marker(language.genus, request)}" /></td>
                    <td>${h.link(request, language)}</td>
                    <td>${h.link_to_map(language)}</td>
                </tr>
                % endfor
            </tbody>
        </table>
    </div>
    % endfor
</div>