- #procesar Markdown
- ```txt

Markdown
========
__TAGS:__ markdown, plain, text, md

For examples on Markdown workflow:

- git/Text-Workflows

Markdown is a plain text format to output HTML. As generator, we use
_marked_, which is JavaScript, runs on Node.js and is the parser that
uses GitHub. It can use the GitHub Flavored Markdown, which is better
suited to work with code than traditional Markdown. There is also
_Pandoc_, an universal document converter.

To install, just try to untar and use. Last time we did something like
this:

    npm install .

inside the Markdown code root.

To use, just:

    bin/marked -i doc.md -o doc.html --gfm --breaks --tables

We also use a CSS called _mardown.css_ for a better visualization of
outputted HTML. For traditional Markdown parsing, use the Perl script
Markdown.pl.

Links
-----
__TAGS:__ markdown, links

Links in Markdown:

```Markdown
This is [an example](http://example.com/ "Title") inline link.

[This link](http://example.net/) has no title attribute.
```

Images
------
__TAGS:__ markdown, images

To add an image:

```Markdown
![Alt text](/path/to/img.jpg)

![Alt text](/path/to/img.jpg "Optional title")
```

Also in reference:

```Markdown
![Alt text][id]

[id]: url/to/image "Optional title here"
```

For PDF, this is the header that sets hyphenation properties and graphic
insertion options:

```LaTeX
\usepackage{graphicx}
\setkeys{Gin}{width=\linewidth}
```

Set images at 300 DPI. Resize as needed with GIMP (not with Gwenview).

Foot Notes
----------
__TAGS:__ markdown, foot, notes

To add a foot note:

```Markdown
This is a foot note[^1]

[^1]:
This is the foot note.
```
```

# Markdown

Markdown is a plain text format for document definition. Use **Pandoc**, an universal document converter.


## Pandoc Recipes

Some Pandoc Markdown recipes:

```Shell
# Convert to DOCX

pandoc -s -f gfm -t docx \
markdown.md > markdown.docx

# Convert to HTML with embedded CSS

pandoc -s --toc -H pandoc.css -f gfm -t html \
markdown.md > markdown.html

# Convert to HTML with CSS linked

pandoc -s --toc --css pandoc.css -f gfm -t html \
markdown.md > markdown.html
```

**-s** makes Pandoc to use the default template to compose the document, for example, it adds encoding information to the generated HTML. To check the default template:

```Shell
pandoc -D html
```

For linking CSS the CSS file must be written normally, but for embedding it the **-H** option put it into the HTML header, so the CSS must be encapsulated in a **<style>** block:

```HTML
<style type="text/css">

/*
 * I add this to html files generated with pandoc.
 */

html {
  font-size: 100%;
  overflow-y: scroll;
  -webkit-text-size-adjust: 100%;
  -ms-text-size-adjust: 100%;
}

body {
  color: #444;
  font-family: Georgia, Palatino, 'Palatino Linotype', Times, 'Times New Roman', serif;
  font-size: 12px;
  line-height: 1.7;
  padding: 1em;
  margin: auto;
  max-width: 42em;
  background: #fefefe;
}

</style>
```


## Links

Links in Markdown:

```Markdown
This is [an example](http://example.com/ "Title") inline link.

[This link](http://example.net/) has no title attribute.
```


## Images

To add an image:

```Markdown
![Alt text](/path/to/img.jpg)

![Alt text](/path/to/img.jpg "Optional title")
```

Also in reference:

```Markdown
![Alt text][id]

[id]: url/to/image "Optional title here"
```

For PDF, this is the header that sets hyphenation properties and graphic insertion options:

```LaTeX
\usepackage{graphicx}
\setkeys{Gin}{width=\linewidth}
```

Set images at 300 DPI. Resize as needed with GIMP (not with Gwenview).


## Foot Notes

To add a foot note:

```Markdown
This is a foot note[^1]

[^1]:
This is the foot note.
```


## Marked

Marked is a Node.js Markdown generator to HTML used by GitHub.

To use, just:

```Shell
bin/marked -i doc.md -o doc.html --gfm --breaks --tables
```

We also use a CSS called **mardown.css** for a better visualization of outputted HTML. For traditional Markdown parsing, use the Perl script Markdown.pl.
