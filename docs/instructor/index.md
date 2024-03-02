# Instructor 


## Create toy files for exercises

```{eval-rst}
.. click:: cspt.cli:createtoyfiles
   :prog: cspt createtoyfiles
   :nested: full
   :commands:

```

## Export lesson plan into different formats. 

Source is myst  markdown with cell metadata and the `Lesson` class gives it a data structure. 

```{eval-rst}
.. click:: cspt.cli:exportprismia
   :prog: cspt exportprismia
   :nested: full
   :commands:

```


```{eval-rst}
.. click:: cspt.cli:exporthandout
   :prog: cspt exporthandout
   :nested: full
   :commands:

```

## Prepare content for the website

For use in preparing notes to post

```{eval-rst}
.. click:: cspt.cli:processexport
   :prog: cspt processexport
   :nested: full
   :commands:

```

```{eval-rst}
.. click:: cspt.cli:exportac
   :prog: cspt exportac
   :nested: full
   :commands:

```

