<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">Feature ${ctx.id}: ${ctx.name}</%block>

<%block name="head">
    <link href="${request.static_url('clld:web/static/css/select2.css')}" rel="stylesheet">
    <script src="${request.static_url('clld:web/static/js/select2.js')}"></script>
</%block>

<div class="span4" style="float: right; margin-top: 1em;">
    <%util:well title="Values">
        <table class="table table-condensed">
            % for de in ctx.domain:
            <tr>
                <%util:iconselect id="iconselect${str(de.number)}" param="v${str(de.number)}">
                    ${h.map_marker_img(req, de)}
                </%util:iconselect>
                <td>${de}</td>
                <td class="right">${len(de.values)}</td>
            </tr>
            % endfor
        </table>
    </%util:well>
</div>

<h2>Feature ${ctx.id}: ${ctx.name}</h2>

<div>${h.alt_representations(req, ctx, doc_position='right', exclude=['snippet.html'])|n}</div>

<p>
    This feature is described in the text of chapter ${ctx.chapter.id}
    <a class="button btn" href="${request.resource_url(ctx.chapter)}">${ctx.chapter.name}</a>
    by ${h.linked_contributors(request, ctx.chapter)}
    ${h.cite_button(request, ctx.chapter)}
</p>
<div>
    <form action="${request.route_url('select_combination')}">
        <fieldset>
            <p>
                You may combine this feature with another one. Start typing the
                feature name or number in the field below.
            </p>
            ${select.render()}
            <button class="btn" type="submit">Submit</button>
        </fieldset>
    </form>
</div>

<br style="clear: right"/>

% if request.map:
${request.map.render()}
% endif

${util.values_and_sentences()}

<%block name="javascript">
wals_parameter_map_on_init = function (map) {
% if ctx.id == '141A':
    L.imageOverlay(
        "${request.static_url('wals3:static/data/141/consonantal.png')}",
        [[3.49339400000014-1, -17.105278], [39.8190167936149-1, 77.8239290000001]]).addTo(map.map);
    L.imageOverlay(
        "${request.static_url('wals3:static/data/141/alphasyllabic.png')}",
        [[3.406389-1, 32.991104], [36.5295501389603-1, 107.695251]]).addTo(map.map);
    L.imageOverlay(
        "${request.static_url('wals3:static/data/141/logographic.png')}",
        [[4.18769799264833-1, 73.446647817425], [53.5745017255304-1, 135.083884328746]]).addTo(map.map);
    L.imageOverlay(
        "${request.static_url('wals3:static/data/141/mixed_logographic_syllabic.png')}",
        [[24.250832-1, 122.935257], [45.5094924891366-1, 153.96579]]).addTo(map.map);
% endif
}
</%block>

