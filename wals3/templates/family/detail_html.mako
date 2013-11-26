<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">Family ${ctx.name}</%block>

<%! from sqlalchemy.orm import joinedload %>
<%! from wals3.models import Genus %>

<ul class="nav nav-pills pull-right">
    <li><a href="#map-container">Map</a></li>
    <li><a href="#list-container">Genera</a></li>
</ul>

<h2>Family ${ctx.name}</h2>

${request.map.render()}

<h3>Genera</h3>
<div id="list-container" class="row-fluid">
    % for genera in u.partitioned(h.DBSession.query(Genus).filter(Genus.family_pk == ctx.pk).order_by(Genus.name).options(joinedload(Genus.languages)).all()):
    <div class="span4">
        % for genus in filter(None, genera):
        <h4>
            <button title="click to toggle display of languages for genus ${genus.name}"
                    type="button" class="btn btn-mini expand-collapse" data-toggle="collapse" data-target="#genus-${genus.pk}">
                <i class="icon icon-plus"> </i>
            </button>
            <img height="20" width="20" src="${u.wals3.map_marker(genus, request)}"
                 id="iconselect${genus.id}" data-toggle="popover" data-placement="right" />
            ${h.link(request, genus)}
            (${str(len(genus.languages))})
        </h4>
        <div id="genus-${genus.pk}" class="collapse">
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
        </div>
        % endfor
    </div>
    % endfor
</div>
<script>
$(document).ready(function() {
    $('.expand-collapse').click(function(){ //you can give id or class name here for $('button')
        $(this).children('i').toggleClass('icon-minus icon-plus');
    });
    % for genus in ctx.genera:
    $('#iconselect${genus.id}').clickover({'html': true, 'content': '${u.icons(request, genus.id)|n}'});
    % endfor
});
</script>
