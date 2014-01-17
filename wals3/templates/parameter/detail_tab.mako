<% citation = h.get_adapter(h.interfaces.IRepresentation, ctx.chapter, request, ext='md.txt') %>${citation.render(ctx.chapter, request)|n}

wals code	name	value	description	latitude	longitude	genus	family	area
% for vs in sorted(datapoints, key=lambda i: i.language.name):
${vs.language.id}	${vs.language.name|n}	${vs.values[0].domainelement.number}	${vs.values[0].domainelement.name|n}	${vs.language.latitude}	${vs.language.longitude}	${vs.language.genus.name|n}	${vs.language.genus.family.name|n}	${ctx.chapter.area.name|n}
% endfor
