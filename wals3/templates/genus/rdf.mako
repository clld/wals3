<%inherit file="../resource_rdf.mako"/>
<%block name="properties">
    <rdf:type rdf:resource="${str(h.rdf.NAMESPACES['skos']['Concept'])}"/>
    % for m in ctx.languages:
    <skos:narrower rdf:resource="${request.resource_url(m)}"/>
    % endfor
    <skos:broader rdf:resource="${request.resource_url(ctx.family)}"/>
</%block>
