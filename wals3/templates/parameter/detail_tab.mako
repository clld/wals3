<% citation = h.get_adapter(h.interfaces.IRepresentation, ctx.chapter, request, ext='md.txt') %>${citation.render(ctx.chapter, request)}

wals code	name	value	description	latitude	longitude	genus	family	area
% for vs in sorted(datapoints, key=lambda i: i.language.name):
${vs.language.id}	${vs.language.name}	${vs.values[0].domainelement.number}	${vs.values[0].domainelement.name}	${vs.language.latitude}	${vs.language.longitude}	${vs.language.genus.name}	${vs.language.genus.family.name}	${ctx.chapter.area.name}
% endfor
