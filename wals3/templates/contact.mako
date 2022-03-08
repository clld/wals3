<%inherit file="home_comp.mako"/>

<h3>${_('Contact')} ${h.contactmail(req)}</h3>
<div class="well">
    <p>${_('You can contact us via email at')} <a href="mailto:${request.contact_email_address}">${request.contact_email_address}</a>.</p>
    % if request.registry.settings.get('clld.github_repos') and request.registry.settings.get('clld.github_repos_data'):
    <% srepo = request.registry.settings['clld.github_repos'] %>
    <% drepo = request.registry.settings['clld.github_repos_data'] %>
    <p><a href="https://github.com">GitHub</a> users can also create and discuss bug reports using the following <strong>issue trackers</strong>:</p>
        <ul>
            <li><a href="https://github.com/${drepo}/issues">${drepo}/issues</a> for errata regarding the site content</li>
            <li><a href="https://github.com/${srepo}/issues">${srepo}/issues</a> for problems with the site software</li>
        </ul>
    % endif
</div>

<h3>Comments</h3>
<p>
    For more than 10 years WALS Online was supplemented with a blog providing readers with a way to comment on
    the content of WALS. Due to the growing maintenance effort we had to shut this blog down, hoping that the
    feedback channels described above can replace it.
</p>
<p>
    Published comments from the blog are available in <a href="https://en.wikipedia.org/wiki/JSON">JSON format</a>
    at <a href="https://github.com/cldf-datasets/wals/blob/master/etc/comments.json">https://github.com/cldf-datasets/wals/blob/master/etc/comments.json</a>.
    While JSON is fairly "human-readable", it can also be processed using tools such as
    ${h.external_link('https://stedolan.github.io/jq/', label='jq')}. E.g. extracting the text of comments on
    WALS feature 19A can be done by running the following jq command:
</p>
<pre>
    $ cat etc/comments.json | jq -c '.[] | select(.post.title | contains("19A"))' | jq -c .text
    "The claim that Nenets
    has pharyngeal consonants is probably due to misunderstanding or
    mistranslations of the Russian term \"гортанный\" (throat-) or its
    equivalents. According to all standard grammars (see
    http://www.helsinki.fi/~tasalmin/sketch.html#phono also for further
    references), Nenets only has glottal stops (two glottal stop phonemes
    can be distinguished due to different morphophonemic realizations)."
</pre>