<%inherit file="../resource_rdf.mako"/>
<%block name="properties">
    <dcterms:identifier rdf:resource="http://dbpedia.org/resource/ISO_3166-2:${ctx.id.upper()}"/>
    % for m in ctx.languages:
        <dcterms:language rdf:resource="${request.resource_url(m)}"/>
    % endfor
</%block>
