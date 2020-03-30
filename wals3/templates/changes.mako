<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>


<h3>Changes</h3>
<p>
    Several editions of WALS Online have been published since 2008. All editions are available
    as CLDF datasets on
    ${h.external_link('https://github.com/cldf-datasets/wals/releases', label='GitHub')}
    as well as via
    ${h.external_link('https://doi.org/10.5281/zenodo.3606197', label='DOI: 10.5281/zenodo.3606197')}
    on Zenodo (listed under the heading "Versions").
</p>
<p>
    Changes of WALS data between editions are tracked via
    ${h.external_link('https://github.com/cldf-datasets/wals/issues', label='issues on GitHub')}.
</p>

<%util:section title="WALS Online 2013 (with minor corrections as of 2020)" id="e2020" level="${4}">
    <p>
        <a href="https://doi.org/10.5281/zenodo.3731125"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.3731125.svg" alt="DOI"></a>
    </p>
    <p>
        See
        ${h.external_link('https://github.com/cldf-datasets/wals/compare/v2014...v2020', label="the diff on GitHub")}
        for details.
    </p>
</%util:section>

<%util:section title="WALS Online 2013 (with minor corrections as of 2014)" id="e2014" level="${4}">
    <p>
        <a href="https://doi.org/10.5281/zenodo.3607439"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.3607439.svg" alt="DOI"></a>
    </p>
    <p>
        Three value assignments have been corrected and
        small corrections have been made to the classification mainly triggered by updates in
        Glottolog's classification.
    </p>
    <p>
        See
        ${h.external_link('https://github.com/cldf-datasets/wals/compare/v2013...v2014', label="the diff on GitHub")}
        for details.
    </p>
</%util:section>

<%util:section title="WALS Online 2013" id="e2013" level="${4}">
    <p>
        <a href="https://doi.org/10.5281/zenodo.3607047"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.3607047.svg" alt="DOI"></a>
    </p>
    <p>
        Several datapoints have been removed (typically because they had been assigned to the
        wrong language, thus they show up as additions above).
    </p>
    <p>
        See
        ${h.external_link('https://github.com/cldf-datasets/wals/compare/v2011...v2013', label="the diff on GitHub")}
        for details.
    </p>
</%util:section>

<%util:section title="WALS Online 2011" id="e2011" level="${4}">
    <p>
        <a href="https://doi.org/10.5281/zenodo.3606403"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.3606403.svg" alt="DOI"></a>
    </p>
    <ul>
        <li>
            There are two new chapters (chapter 143 on Order of Negative Morpheme and Verb, and
            chapter 144 on Position of Negative Word With Respect to Subject, Object, and Verb,
            both with many new maps)
        </li>
        <li>
            Additional features have been added to some chapters.
        </li>
        <li>
            The genealogical classification of languages, including genera, has been updated.
        </li>
        <li>
            The one-to-many relationship between chapters and features/maps is now clearly reflected
            in the structure of WALS: A single chapter can contain not just one feature, but several
            features, most often two (e.g. feature 39A and feature 39B), but sometimes (with the new
            chapters 143 and 144) quite a few features and maps.
        </li>
        <li>
            For some of the features, WALS now includes examples supplied by the authors (for example feature 113A)
        </li>
        <li>
            WALS Online now contains the long introduction chapter of the printed atlas from 2005
        </li>
    </ul>
    <p>
        See
        ${h.external_link('https://github.com/cldf-datasets/wals/compare/v2008...v2011', label="the diff on GitHub")}
        for details.
    </p>
</%util:section>

<%util:section title="WALS Online 2008" id="e2008" level="${4}">
    <p>
        <a href="https://doi.org/10.5281/zenodo.3606198"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.3606198.svg" alt="DOI"></a>
    </p>
    <p>
        A description of errate in the printed version of 2005 can be found at
        ${h.external_link('http://blog.wals.info/category/errata/errata-2005/')}.
    </p>
</%util:section>
