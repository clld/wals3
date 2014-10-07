<%inherit file="../wals3.mako"/>
<%namespace name="util" file="../util.mako"/>
<%namespace name="lib" file="../lib.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Combination')} ${ctx.name}</%block>

<h3>${_('Combination')} ${' / '.join(h.link(request, p) for p in ctx.parameters)|n}</h3>

% if len(ctx.parameters) < 4:
<div>
    <form action="${request.route_url('select_combination')}">
        <fieldset>
            <p>
                You may combine these features with another one. Start typing the
                feature name in the field below.
            </p>
            ${select.render()}
            <button class="btn" type="submit">Submit</button>
        </fieldset>
    </form>
</div>
% endif

% if map:
${map.render()}
% endif

% if ctx.domain:
<div id="list-container">
    <%util:table items="${enumerate(ctx.domain)}" args="item" eid="refs" class_="table-condensed table-striped table-nonfluid" options="${dict(aaSorting=[[2, 'desc']])}">\
    <%def name="head()">
        <th> </th>
        <th> </th>
        <th>${' / '.join(h.link(request, p) for p in ctx.parameters)|n}</th>
        <th>Number of languages</th>
    </%def>
    <td>
        % if item[1].languages:
            <button title="click to toggle display of languages for value ${item[1].name}"
                    type="button" class="btn btn-mini expand-collapse" data-toggle="collapse" data-target="#de-${item[0]}">
                <i class="icon icon-plus"> </i>
            </button>
        % endif
    </td>
    <td>
        % if item[1].languages:
            <img height="20" width="20" src="${item[1].icon.url(request)}"/>
        % endif
    </td>
    <td>
        ${item[1].name}
        <div id="de-${item[0]}" class="collapse">
            <table class="table table-condensed table-nonfluid">
                <tbody>
                    % for language in item[1].languages:
                        <tr>
                            <td>${h.link_to_map(language)}</td>
                            <td>${h.link(request, language)}</td>
                        </tr>
                    % endfor
                </tbody>
            </table>
        </div>
    </td>
    <td style="text-align: right;">${str(len(item[1].languages))}</td>
    </%util:table>
</div>
<script>
$(document).ready(function() {
    $('.expand-collapse').click(function(){ //you can give id or class name here for $('button')
        $(this).children('i').toggleClass('icon-minus icon-plus');
    });
});
</script>
% endif

<%block name="head">
    <link href="${request.static_url('clld:web/static/css/select2.css')}" rel="stylesheet">
    <script src="${request.static_url('clld:web/static/js/select2.js')}"></script>
</%block>
