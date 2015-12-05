$(document).ready(function() {

    repos_to_monitor = [
        {"owner": "mila-udem", "repo": "blocks"},
        {"owner": "mila-udem", "repo": "fuel"},
        {"owner": "mila-udem", "repo": "blocks-examples"}
    ];
    repo_roster = [];
    for (var i=0, tot=repos_to_monitor.length; i < tot; i++) {
        $.get("/repo_roster/"+repos_to_monitor[i]["owner"]+"/"+repos_to_monitor[i]["repo"], function(data) {
            repo_roster.push(data);

            // this should be refactored at some point...
            if (repo_roster.length === 3) {
                items = [];
                // thanks http://stackoverflow.com/questions/1208467/how-to-add-items-to-a-unordered-list-ul-using-jquery
                $.each(repo_roster, function(i, repo) {
                    var comments = "<ul class=comments-dropdown><li><a href=''>"
                                   + repo["comments"].length
                                   + " comments</a><ul>"
                    // for loop here
                    for (j=0; j < repo["comments"].length; j++) {
                        var current_comment = repo["comments"][j];
                        var current_comment_html = (
                             "<li class='hidden'>"
                           + "<a href='" + current_comment["url"] + "'>"
                           + current_comment["body"]
                           + "</a></li>"
                        )
                        comments = comments + current_comment_html
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
                                // # of comments
                                // + repo["comments"].length
                                // + ' comments'

                                + '</li>');
                });  // close each()

                $('#repo-roster').append(items.join(''));
                // $('.comments-dropdown').dropit();
            }
        });
    }
});

$('.comments-dropdown').click(function(event) {
    debugger;
});