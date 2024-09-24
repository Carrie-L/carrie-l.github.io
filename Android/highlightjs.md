---
layout: android
title: anki 高亮代码
tags: ["anki","教程"]
category: Android
---


https://highlightjs.org/demo
------------------------------------------
背面内容模板，添加到回答<div>后面

```html
<link href="_tokyo-night-dark.css" rel="stylesheet">
<script src="_highlight.min.js"></script>
<script>
  document.querySelectorAll('code').forEach(function (block) {
    block.innerHTML = block.innerHTML.replace(/&amp;nbsp;/g, ' ');
  });
  hljs.highlightAll();
</script>
```



<script src="_highlight.min.js"></script>
<script>
  document.querySelectorAll('code').forEach(function (block) {
    block.innerHTML = block.innerHTML.replace(/&amp;nbsp;/g, ' ');
  });
  hljs.highlightAll();
</script>
------------------------------------------------
添加到样式CSS：

```css
pre code {
  background: #1a1b26;
  color: #9aa5ce;
  padding: 10px;
  border-radius: 5px;
  display: block;
  white-space: pre-wrap;
}

code {
  font-family: Consolas, Monaco, "Andale Mono", "Ubuntu Mono", monospace;
  font-size: 14px;
}

```

