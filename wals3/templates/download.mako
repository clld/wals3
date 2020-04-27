<%inherit file="home_comp.mako"/>
<%namespace name="mpg" file="clldmpg_util.mako"/>

<%block name="head">
    <style>
        a.accordion-toggle {
            font-weight: bold;
        }
    </style>
</%block>

<h3>Downloads</h3>

<div class="alert alert-info">
    <p>
        WALS Online serves the latest
        ${h.external_link('https://github.com/cldf-datasets/wals/releases', label='released version')}
        of data curated at
        ${h.external_link('https://github.com/cldf-datasets/wals', label='cldf-datasets/wals')}.
        Older released version are accessible via <br/>
        <a href="https://doi.org/10.5281/zenodo.3606197"><img
                src="https://zenodo.org/badge/DOI/10.5281/zenodo.3606197.svg" alt="DOI"></a>
        <br/>
        on ZENODO as well.
    </p>
</div>
