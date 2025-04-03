---
layout: default
title: Tools & Resources
---

<input type="text" id="search" placeholder="Search tools..." />

<select id="category-filter">
  <option value="all">All Categories</option>
  {% assign categories = site.tools | map: "category" | uniq %}
  {% for category in categories %}
  <option value="{{ category }}">{{ category | capitalize }}</option>
  {% endfor %}
</select>

<ul id="tool-list">
  {% for tool in site.tools %}
  <li data-title="{{ tool.title }}" data-category="{{ tool.category }}" data-tags="{{ tool.tags | join: ',' }}">
    <a href="{{ tool.link }}">{{ tool.title }}</a> - {{ tool.description }}
  </li>
  {% endfor %}
</ul>

<script src="https://cdnjs.cloudflare.com/ajax/libs/lunr.js/2.3.9/lunr.min.js"></script>
<script>
  let tools = [
    {% for tool in site.tools %}
    {
      title: "{{ tool.title }}",
      category: "{{ tool.category }}",
      description: "{{ tool.description }}",
      tags: "{{ tool.tags | join: ' ' }}",
      link: "{{ tool.link }}"
    },
    {% endfor %}
  ];

  let idx = lunr(function () {
    this.ref("link");
    this.field("title");
    this.field("category");
    this.field("description");
    this.field("tags");

    tools.forEach(doc => this.add(doc));
  });

  function filterTools() {
    let query = document.getElementById("search").value.toLowerCase();
    let category = document.getElementById("category-filter").value;
    let list = document.getElementById("tool-list");
    list.innerHTML = "";

    let filtered = tools.filter(tool => 
      (category === "all" || tool.category === category) &&
      (query === "" || tool.title.toLowerCase().includes(query) || tool.tags.toLowerCase().includes(query))
    );

    filtered.forEach(tool => {
      let li = document.createElement("li");
      li.innerHTML = `<a href="${tool.link}">${tool.title}</a> - ${tool.description}`;
      list.appendChild(li);
    });
  }

  document.getElementById("search").addEventListener("input", filterTools);
  document.getElementById("category-filter").addEventListener("change", filterTools);
</script>

<h2>Contributors</h2>

<ul id="contributors-list"></ul>

<script>
  const repoOwner = "UCT-datastewardship";  // Change this
  const repoName = "UCT-datastewardship.github.io";  // Change this
  const sinceDate = "2025-01-01T00:00:00Z";  // Filter from this date forward

  async function fetchContributorsSinceDate() {
    try {
      const response = await fetch(`https://api.github.com/repos/${repoOwner}/${repoName}/commits?since=${sinceDate}`);
      const commits = await response.json();

      let contributors = new Map();  // Store users and first commit date

      for (const commit of commits) {
        const author = commit.author;
        if (author && !contributors.has(author.login)) {
          contributors.set(author.login, {
            username: author.login,
            profile: author.html_url,
            firstCommitDate: commit.commit.author.date
          });
        }
      }

      const list = document.getElementById("contributors-list");
      list.innerHTML = "";

      contributors.forEach(user => {
        let li = document.createElement("li");
        li.innerHTML = `<a href="${user.profile}" target="_blank">${user.username}</a> (since ${new Date(user.firstCommitDate).toDateString()})`;
        list.appendChild(li);
      });

    } catch (error) {
      console.error("Failed to load contributors", error);
    }
  }

  fetchContributorsSinceDate();
</script>
