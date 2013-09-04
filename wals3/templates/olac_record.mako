<%def name="record(obj)">
  <olac:olac xmlns:olac="http://www.language-archives.org/OLAC/1.1/"
           xmlns:dc="http://purl.org/dc/elements/1.1/"
           xmlns:dcterms="http://purl.org/dc/terms/"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.language-archives.org/OLAC/1.1/ http://www.language-archives.org/OLAC/1.1/olac.xsd">
    <dc:identifier xsi:type="dcterms:URI">${request.resource_url(obj)}</dc:identifier>
    <dc:type xsi:type="dcterms:DCMIType">Text</dc:type>
    <dc:format xsi:type="dcterms:IMT">text/html</dc:format>
    <dc:date xsi:type="dcterms:W3CDTF">${date(obj.updated)}</dc:date>
    <dc:type xsi:type="olac:linguistic-type" olac:code="language_description"/>
    % if isinstance(obj, h.models.Source):
    <dc:title>${obj.description}</dc:title>
    <dcterms:bibliographicCitation>
      ${obj.bibtex().text()|n}
    </dcterms:bibliographicCitation>
    <dc:creator>${obj.author}</dc:creator>

    % for c in obj.contributionreferences:
    <dcterms:isReferencedBy>${request.resource_url(c.contribution)}</dcterms:isReferencedBy>
    % endfor

    % for l in filter(lambda l: l.iso_code, obj.languages):
    <dc:subject olac:code="${l.iso_code}" xsi:type="olac:language" />
    % endfor

    ## TODO: publisher, subject (including olac_subject), year

    ##${dc_unqualified(record)}
    ##<dcterms:isPartOf py:if="record.fetchone('booktitle')">${record.fetchone('booktitle')}</dcterms:isPartOf>

    ##<dc:subject py:for="code in record.fetchall('olac_field')" olac:code="${code}" xsi:type="olac:linguistic-field">${h.OLAC_LINGUISTIC_FIELD_MAP.get(code, code)}</dc:subject>

    % else:
    <dc:title>${request.dataset} Resources for ${obj}</dc:title>
    ##<dc:contributor xsi:type="olac:role" olac:code="editor" py:for="contrib in c.contribs">${contrib}</dc:contributor>
    <dc:description>
      A page listing all resources in ${request.dataset} which are relevant to the language ${obj}.
    </dc:description>
    <dc:publisher>${request.dataset.publisher_name}</dc:publisher>
    <dc:language xsi:type="olac:language" olac:code="eng"/>
    <dc:subject xsi:type="olac:language" olac:code="${obj.iso_code}"/>
    % endif
  </olac:olac>
</%def>
