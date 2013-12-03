<?xml version="1.0" encoding="utf-8"?>
<kml xmlns="http://earth.google.com/kml/2.1" xmlns:wals="http://wals.info/" xmlns:atom="http://www.w3.org/2005/Atom">
  <Document>
    <name>${ctx.name}</name>
    <atom:author>
      <atom:name><span xmlns="http://www.w3.org/1999/xhtml" class="authors">
      <span class="prefix">by </span>${ctx.chapter.formatted_contributors()}</span></atom:name>
    </atom:author>
    <open>1</open>
    <description>
      <![CDATA[
      Values for language feature ${h.link(request, ctx)} from ${h.link(request, request.dataset)}.
      ]]>
    </description>
    <atom:link href="${request.resource_url(ctx, ext='kml')}"/>
    <TimeStamp><when>${ctx.updated.isoformat().split('+')[0]}Z</when></TimeStamp>
    <ExtendedData>
      <wals:type>feature</wals:type>
      <wals:id>${ctx.id}</wals:id>
      <wals:base_url>${request.resource_url(request.dataset)}</wals:base_url>
    </ExtendedData>
    % for de in ctx.domain:
    <Style id="s${de.pk}">
      <IconStyle>
        <color>7f${de.jsondata['icon'][1:]}</color>
        <scale>0.50</scale>
        <Icon><href>${request.static_url('clld:web/static/icons/' + de.jsondata['icon'] + '.png')}</href></Icon>
      </IconStyle>
    </Style>
    % endfor
    % for de in ctx.domain:
    <Folder>
      <name>${de.name}</name>
      <description>Placemarks for value "${de.name}"</description>
      <ExtendedData>
        <wals:value>${de.number}</wals:value>
      </ExtendedData>
      % for vs in sorted(filter(lambda dp: dp.values[0].domainelement_pk == de.pk, datapoints), key=lambda i: i.language.name):
      <Placemark>
        <name>${vs.language.name}</name>
        <description>
          <![CDATA[
          ${h.link(request, vs.language)}: Feature ${h.link(request, ctx)}
          (value "${vs.values[0].domainelement.name}")
          ]]>
        </description>
        <ExtendedData>
          <wals:code>${vs.language.id}</wals:code>
        </ExtendedData>
        <Point>
          <coordinates>${vs.language.longitude},${vs.language.latitude} </coordinates>
        </Point>
        <styleUrl>#s${de.pk}</styleUrl>
      </Placemark>
      % endfor
    </Folder>
    % endfor
  </Document>
</kml>
