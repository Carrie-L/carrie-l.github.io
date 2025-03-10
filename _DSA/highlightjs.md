---
layout: article
title: "highlightjs"
date: 2024-10-13
tags: ["DSA"]
permalink: /dsa/highlightjs/
---

---
layout: article
title: anki 高亮代码
tags: []
category: DSA
---

 样式地址
https://highlightjs.org/demo

 背面
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

```html
<script src="_highlight.min.js"></script>
<script>
  document.querySelectorAll('code').forEach(function (block) {
    block.innerHTML = block.innerHTML.replace(/&amp;nbsp;/g, ' ');
  });
  hljs.highlightAll();
</script>
```
---------------------------
---

---

---

---

---

---

---

添加到样式CSS：

```css
pre code {
  background: 
  color: 
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

