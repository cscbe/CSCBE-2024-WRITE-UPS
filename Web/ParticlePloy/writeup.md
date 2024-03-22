## temporary writeup summary

- greeted with a form to create a custom particle visualisation
- filling in the form we see that we get redirected to a page with uuid in the path that show a particle system that
  matches the parameters we filled. We also entered a name at the top of the form which is shown on the second 'view'
  page.
- A note at the bottom says that admin's will look at the pages to review them.
- looking at the source we see that on our 'view' page a custom javascript file is loaded instead of the default one. This custom javascript file reflects the custom parameters we entered.
- We try to enter strange and unexpected values in the form. We see that everything is very strictly validated except the name input.
- The name is not used in the javascript so we cannot use it to inject javascript.
- Entering any kind of script tag in the name is also sanitized.
- A special thing is still how the script tag is created at the bottom. It looks at `window.config` which is set at the top of the page.
- We find that we could maybe clobber the dom by using some special attributes in the name input.
- We can try a <a> element with a `href` attribute. If the toString function is called on it it will just return the `href`.
- 