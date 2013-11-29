<?xml version="1.0" encoding="utf-8"?>
<feature number="${ctx.id}" base_url="${request.resource_url(request.dataset)}" name="${ctx.name}">
  <description>
    <url>${request.resource_url(ctx, ext='xml')}</url>
    <timestamp>${ctx.updated.isoformat()}</timestamp>
  </description>
    % for de in ctx.domain:
    <v numeric="${de.number}" description="${de.name|x}" icon_id="${de.jsondata['icon']}" icon_url="${request.static_url('clld:web/static/icons/' + de.jsondata['icon'] + '.png')}" zindex="0">
      % for vs in sorted(filter(lambda dp: dp.values[0].domainelement_pk == de.pk, datapoints), key=lambda i: i.language.name):
      <l c="${vs.language.id}" n="${vs.language.name|x}" lng="${vs.language.longitude}" lat="${vs.language.latitude}"/>
      % endfor
  </v>
    % endfor
</feature>
