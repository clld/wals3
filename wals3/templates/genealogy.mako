<%inherit file="wals3.mako"/>
<%namespace name="util" file="util.mako"/>
<%namespace name="lib" file="lib.mako"/>

<%! active_menu_item = "languages" %>
<%block name="title">Genealogy</%block>

<%def name="sidebar()">
    <%util:well>
      <p>
        This section gives a list of the languages that appear on at least one map in the atlas, organized
        according to their genealogical classification. The classification here does not include many
        intermediate groupings that appear in Ethnologue (<a class="Reference"
        href="http://wals.info/refdb/record/Grimes-2000" title="view reference details">Grimes 2000</a>) or
        <a class="Reference" href="http://wals.info/refdb/record/Ruhlen-1987" title="view reference
        details">Ruhlen (1987)</a>, restricting to only two levels in the majority of cases, that of family,
        the highest level widely accepted by specialists, and genus, explained presently. In some cases, we
        provide an intermediate level, that of subfamily, where the subfamily is well-known.
      </p>
      <p>
        The notion genus is explained in <a class="Reference" href="http://wals.info/refdb/record/Dryer-1989"
        title="view reference details">Dryer (1989)</a>. It is intended as a level of classification which is
        comparable across the world, so that a genus in one family is intended to be comparable in time depth
        to genera in other parts of the world. The choice of term is intended to match the general idea of
        genus in biological classification, where a genus is a set of species that are clearly closely
        related to each other (and where words in everyday language often correspond to genera rather than
        species). In the genealogical classification of languages, a genus is a group of languages whose
        relatedness is fairly obvious without systematic comparative analysis, and which even the most
        conservative “splitter” would accept. Genealogical groups deeper than a genus are often less obvious
        and in the absence of detailed comparative work are often not universally accepted. If there is
        evidence of time depth of groups, the genus would not have a time depth greater than 3500 or 4000
        years. A genus may have a time depth much less than this, but if the time of the split of one group
        of languages from other languages in the family appears to be greater than 4000 years, then this
        constitutes a reason to say that this group of languages is a separate genus. The standard
        subfamilies of

        Indo-European

        (e.g. Germanic, Slavic, Celtic, etc.) are fairly clear examples of
        genera, although Celtic is perhaps a clearer example than Germanic or Slavic, both of which have a
        time depth considerably less than 3500 years. The decisions as to which groups to treat as genera
        here are best described as my own educated guesses. In many instances they are based on conversations
        he has had with specialists.  However, in the absence of a tradition within the field of attempting
        to identify groups of comparable time depth in different parts of the world, they should not be
        considered more than educated guesses. Specialists who think the choices of genera here are mistaken
        are encouraged to let me know.
      </p>
      <p>
        The classification here generally follows the classification given in <a class="Reference"
        href="http://wals.info/refdb/record/Grimes-2000" title="view reference details">Grimes (2000)</a>,
        the 14th edition of Ethnologue. <!--Footnotes below indicate differences between the WALS
        classification and that in Ethnologue.--> The classification deviates most strongly from that in
        Ethnologue in the classification of the languages of

        New Guinea.

        The Ethnologue classification is a standard one, and is similar to that in <a class="Reference"
        href="http://wals.info/refdb/record/Ruhlen-1987" title="view reference details">Ruhlen (1987)</a>,
        both being largely based on the classification in <a class="Reference"
        href="http://wals.info/refdb/record/Wurm-1975" title="view reference details">Wurm (1975)</a> and <a
        class="Reference" href="http://wals.info/refdb/record/Wurm-1982" title="view reference details">Wurm
        (1982)</a>. However, most specialists are now skeptical of various components of the Wurm
        classification. The classification used here is considerably more conservative than the Wurm
        classification, positing a much larger number of families, and reflects suggestions of William Foley,
        though I accept responsibility for any misinterpretation of his ideas.
      </p>
      <p>
        <!--Each family, subfamily, and genus in the classification below is assigned a numeric code consisting
            of one, two, or three numbers. The first number identifies the family, the second number if there
            are three numbers identifies the subfamily within the family, and the last number identifies the
            genus.  If a family consists of a single genus (as many do in this classification), then the family
            is assigned a single number and it is assumed that this single number identifies the genus as well.-->
        Names of genera are given in italics.  Language isolates are a special case of this: they are
        families that consist not only of only one genus, but also of only one language. There are cases
        here of what are generally considered language isolates but for which more than one variety is
        included in the WALS languages.  When these varieties are all mutually intelligible, then the
        language can be considered a language isolate, though since we do not attempt to systematically
        distinguish languages and dialects, one cannot tell which families
        with more than one language here are language isolates in this sense. Examples of language
        isolates in this sense are

        Basque

        and

        Yukaghir.
      </p>
      <p>
        <!--The families are organized here in a roughly geographical fashion, starting in southern Africa and
            ending, except for the last two groups, in southern South America.  The order is similar in spirit,
            but different in detail, from that in Ruhlen (1987).-->
        Within each family, the subfamilies and genera
        are organized alphabetically, and within each genus, the languages are organized alphabetically.
        Two groups here are not genealogical groups. The first of these is Creoles and Pidgins,
        whose nature falls outside standard genealogical classification.  The last is Sign Languages. Here
        the notion of genealogical classification makes sense, but crosslinguistic work on sign languages
        is sufficiently new that it would be premature to attempt a genealogical classification of them.
      </p>
    </%util:well>
</%def>

${lib.languages_contextnav()}

<h2>Genealogical Language List</h2>
##
## TODO:
## - by Matthew Dryer
## - counts of languages, genera, families
##
<div class="btn-toolbar">
  <div class="btn-group">
    <button onclick="CLLD.TreeView.show(1);" class="btn">Show Genera</button>
    <button onclick="CLLD.TreeView.hide(1);" class="btn">Hide Genera</button>
  </div>
  <div class="btn-group">
    <button onclick="CLLD.TreeView.show(2);" class="btn">Show Languages</button>
    <button onclick="CLLD.TreeView.hide(2);" class="btn">Hide Languages</button>
  </div>
</div>
<div class="treeview">
  <ul>
    % for family in families:
    <li>
      <%util:tree_node_label level="1" id="f-${family.id}" checked="${False}">
        ${h.link(request, family)}
      </%util:tree_node_label>
      <ul>
        % for genus in family.genera:
        <li>
          <%util:tree_node_label level="2" id="g-${genus.id}">
            ${h.link(request, genus)}${' (subfamily: '+genus.subfamily+')' if genus.subfamily else ''}
          </%util:tree_node_label>
          <ul>
            % for language in genus.languages:
            <li>${h.link(request, language)}</li>
            % endfor
          </ul>
        </li>
        % endfor
      </ul>
    </li>
    % endfor
  </ul>
</div>
<script>
$(document).ready(function() {
  CLLD.TreeView.init();
});
</script>
