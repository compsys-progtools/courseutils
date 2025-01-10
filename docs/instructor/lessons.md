# Lesson Management


## Export lesson plan into different formats. 

Source is myst  markdown with cell metadata and the `Lesson` class gives it a data structure. 

## Prismia

- Run command (typially redirected to a file)
- copy file contents
- go to lessons
- create new, add title
- click the plus sign
- paste in prismia
- press escape then shift + `m` 
- then click split
during class:

select messages from the lesson button

[guide](https://prismia.chat/guide)

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
