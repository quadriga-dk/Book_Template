# H5P standalone activities

Put standalone H5P activities in this directory so Jupyter Book copies them to
the published GitHub Pages site without mixing them into the regular `_static`
assets.

For each activity, create this structure:

```text
_static_h5p/
  h5p/
    my-activity/
      index.html
      content/
        h5p.json
        content/
        libraries/
      dist/
        main.bundle.js
        frame.bundle.js
        styles/
          h5p.css
```

Build output:

```text
_build/html/h5p/my-activity/index.html
```

Published URL:

```text
https://quadriga-dk.github.io/Book_Template/h5p/my-activity/index.html
```

To add an activity:

1. Download a release of `tunapanda/h5p-standalone`.
2. Copy its `dist/` folder into the activity folder.
3. Rename the `.h5p` file to `.zip`.
4. Extract the archive into the activity folder as `content/`.
5. Copy `_static_h5p/h5p/_template/index.html` into the activity folder.
6. Embed the activity in a Jupyter Book Markdown page with an iframe.

