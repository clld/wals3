<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://purl.org/rss/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:georss="http://www.georss.org/georss">
  <channel rdf:about="${request.resource_url(ctx)}">
    <link>${request.resource_url(ctx)}</link>
    <title>${ctx.name}</title>
    <description>Datapoints for feature "${ctx.name}"</description>
    <dc:creator>${ctx.chapter.formatted_contributors()}</dc:creator>
    <dc:date>${ctx.updated.isoformat()}</dc:date>
    <items>
      <rdf:Seq>
        % for vs in datapoints:
        <rdf:li resource="${request.resource_url(vs)}"/>
        % endfor
      </rdf:Seq>
    </items>
  </channel>
  % for vs in datapoints:
  <item rdf:about="${request.resource_url(vs)}">
    <link>${request.resource_url(vs)}</link>
    <title>${vs.language.name}: ${vs.values[0].domainelement.name}</title>
    <description>
      Language ${h.link(request, vs.language)|x}: Feature ${h.link(request, ctx)|x}
      (value "${vs.values[0].domainelement.name}")
    </description>
    <georss:point>${vs.language.latitude} ${vs.language.longitude}</georss:point>
    <dc:date>${vs.values[0].updated.isoformat()}</dc:date>
  </item>
  % endfor
</rdf:RDF>
