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
      <p>Link: <a href="{{ tool.link }}">{{ tool.link }}</a></p>
      <p>Cetegory: <strong>{{ tool.category }}</strong></p>
    </li>
  {% endfor %}
</ul>

<script src="{{ site.baseurl }}/assets/js/search.js"></script>


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
