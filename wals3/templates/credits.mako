<%inherit file="home_comp.mako"/>
<%! from clld_markdown_plugin import markdown %>
<%namespace name="util" file="util.mako"/>

${markdown(req, text)|n}

