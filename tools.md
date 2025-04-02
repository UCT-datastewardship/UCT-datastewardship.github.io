---
layout: default
---

<h1>Tools</h1>

<input type="text" id="search-box" placeholder="Search tools...">

<ul id="tools-list">
  {% for tool in site.tools %}
    <li class="tool-item">
      <h2>{{ tool.title }}</h2>
      <p>{{ tool.description }}</p>
      <a href="{{ tool.link }}">Link</a>
    </li>
  {% endfor %}
</ul>

<script src="{{ site.baseurl }}/assets/js/search.js"></script>
