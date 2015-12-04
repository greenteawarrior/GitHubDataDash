$.getJSON("repo_roster.json", function(repo_roster) {

    items = [];
    // thanks http://stackoverflow.com/questions/1208467/how-to-add-items-to-a-unordered-list-ul-using-jquery
    $.each(repo_roster, function(i, repo) {
        var comments = "<ul class=comments-dropdown><li><a href=''>"
                       + repo["comments"].length
                       + " comments</a><ul>"
        // for loop here
        for (j=0; j < repo["comments"].length; j++) {
            var current_comment = repo["comments"][j];
            comments = comments
                       + "<li>"
                       + "<a href='" + current_comment["url"] + "'>"
                       + current_comment["body"]
                       + "</a></li>"
        }
        comments = comments + "</ul></li></ul>"

        items.push('<li>'

                    // repo name with link
                    + '<a href='
                    + repo["repo_url"] + '>'
                    + repo["repo_name"]
                    + '</a> ||  '

                    // # of pull requests
                    + repo["pull_requests"].length
                    + ' PR ||  '

                    + comments
                    // // # of comments
                    // + repo["comments"].length
                    // + ' comments'

                    + '</li>');
    });  // close each()

    $('#repo-roster').append(items.join(''));
    $('.comments-dropdown').dropit();
});
