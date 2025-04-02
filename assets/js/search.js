document.addEventListener('DOMContentLoaded', function() {
  var searchBox = document.getElementById('search-box');
  var toolsList = document.getElementById('tools-list');
  var tools = toolsList.getElementsByClassName('tool-item');

  searchBox.addEventListener('input', function() {
    var searchTerm = searchBox.value.toLowerCase();

    Array.prototype.forEach.call(tools, function(tool) {
      var title = tool.getElementsByTagName('h2')[0].textContent.toLowerCase();
      var description = tool.getElementsByTagName('p')[0].textContent.toLowerCase();

      if (title.includes(searchTerm) || description.includes(searchTerm)) {
        tool.style.display = '';
      } else {
        tool.style.display = 'none';
      }
    });
  });
});
