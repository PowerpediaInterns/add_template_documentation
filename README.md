# add_template_documentation
Adds the {{documentation}} tag to Templates.

## Class variables for customization
### TEMPLATE
The template that will be used to tag pages (e.g. `<noinclude>\n\n{{documentation}}\n</noinclude>`).

### NAMESPACE
The namespace that the program will extract pages from (e.g. 0 for (Main)).\
https://www.mediawiki.org/wiki/Manual:Namespace#Built-in_namespaces to see available namespaces.

### PAGES_LIMIT
The number of pages that will be extracted at a time. Used in get_params() in params for "aplimit".
