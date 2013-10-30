<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%namespace name="lib" file="../lib.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">Languages</%block>
<%block name="head">
    <link href="${request.static_url('clld:web/static/css/select2.css')}" rel="stylesheet">
    <script src="${request.static_url('clld:web/static/js/select2.js')}"></script>
</%block>

${lib.languages_contextnav()}

<div class="span6 pull-right well well-small">
    <p>
        Search a languoid by name. Matching names are formatted in bold font for
        <b>languages</b>, in italics for <i>genera</i> and underlined for <u>families</u>.
        This search does also take alternative names into account.
    </p>
    ${ms.render()}
</div>

<h2>Languages</h2>

<div class="clearfix"> </div>
${ctx.render()}

<script type="text/javascript">
    $(document).ready(function() {
        $("#${ms.eid}").on("select2-selecting", function(e) {
            document.location.href = '${ms.url}?id=' + e.val;
        });
    });
</script>
