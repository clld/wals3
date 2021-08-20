<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "sources" %>
<%block name="title">${_('Source')} ${ctx.name}</%block>

<h2>${ctx.name}</h2>
${ctx.coins(request)|n}

<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#tab1" data-toggle="tab">Text</a></li>
        <li><a href="#tab2" data-toggle="tab">BibTeX</a></li>
    </ul>
    <div class="tab-content">
        <% bibrec = ctx.bibtex() %>
        <div id="tab1" class="tab-pane active">
            <p id="${h.format_gbs_identifier(ctx)}">${bibrec.text()}</p>
            % if ctx.datadict().get('Additional_information'):
            <p>
                ${ctx.datadict().get('Additional_information')}
            </p>
            % endif
            % if bibrec.get('url'):
                <p>${h.external_link(bibrec['url'])}</p>
            % endif
            ${util.gbs_links(filter(None, [ctx.gbs_identifier]))}
            % if ctx.jsondata.get('internetarchive_id'):
                <hr />
                <iframe src='https://archive.org/stream/${ctx.jsondata.get('internetarchive_id')}?ui=embed#mode/1up' width='680px' height='750px' frameborder='1' ></iframe>
            % endif
        </div>
        <div id="tab2" class="tab-pane"><pre>${bibrec}</pre></div>
    </div>
</div>

<%def name="sidebar()">
    <% referents, one_open = context.get('referents', {}), False %>
    <div class="accordion" id="sidebar-accordion">
    % if referents.get('language'):
        <%util:accordion_group eid="acc-l" parent="sidebar-accordion" title="${_('Languages')}" open="${not one_open}">
            ${util.stacked_links(referents['language'])}
        </%util:accordion_group>
        <% one_open = True %>
    % endif
    % if referents.get('contribution'):
        <%util:accordion_group eid="acc-c" parent="sidebar-accordion" title="${_('Contributions')}" open="${not one_open}">
            ${util.stacked_links(referents['contribution'])}
        </%util:accordion_group>
        <% one_open = True %>
    % endif
    % if referents.get('valueset'):
        <%util:accordion_group eid="acc-v" parent="sidebar-accordion" title="${_('ValueSets')}" open="${not one_open}">
            ${util.stacked_links(referents['valueset'])}
        </%util:accordion_group>
        <% one_open = True %>
    % endif
    % if referents.get('sentence'):
        <%util:accordion_group eid="acc-s" parent="sidebar-accordion" title="${_('Sentences')}" open="${not one_open}">
            ${util.stacked_links(referents['sentence'])}
        </%util:accordion_group>
        <% one_open = True %>
    % endif
    </div>
</%def>
