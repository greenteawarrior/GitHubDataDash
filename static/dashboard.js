$(document).ready(function() {
    // mila-udem repos
    // repos_to_monitor = [
    //     {"owner": "mila-udem", "repo": "blocks"},
    //     {"owner": "mila-udem", "repo": "fuel"},
    //     {"owner": "mila-udem", "repo": "blocks-examples"}
    // ];
    repos_to_monitor = [
        {"owner": "OlinMobileProto", "repo": "Lab1"},
        {"owner": "OlinMobileProto", "repo": "Lab2"}
    ];
    repo_roster = [];
    for (var i=0, tot=repos_to_monitor.length; i < tot; i++) {
        $.get("/repo_roster/"+repos_to_monitor[i]["owner"]+"/"+repos_to_monitor[i]["repo"], function(data) {
            repo_roster.push(data);

            if (repo_roster.length === repos_to_monitor.length) {
                items = [];
                comments_roster = {};
                // thanks http://stackoverflow.com/questions/1208467/how-to-add-items-to-a-unordered-list-ul-using-jquery
                $.each(repo_roster, function(i, repo) {
                    var comments ='<ul class="list-group">';

                    for (j=0; j < repo["comments"].length ; j++) {
                        var current_comment = repo["comments"][j];
                        var current_comment_html = (
                             "<li class='hidden list-group-item col-xs-12'>"
                            + '<div class="col-md-2"><img style="width:90px" src="' + current_comment['avatar_url'] + '&s=90' + '"><br>' + current_comment["person"] + '</div>'
                            + '<div class="col-md-10">' + markdown.toHTML(current_comment["body"]) + '</div>'
                            + '<a href="' + current_comment["url"] + '">'

                            + '<div class="col-xs-12" style="padding: 0">'
                            + '<div class="col-md-2"></div>'
                            + '<div class="col-md-10" style="padding-right: 20"><button class="btn btn-primary">View comment + PR on GitHub</button></a></div>'
                            + '</li>'
                        )
                        comments = comments + current_comment_html;
                    }
                    comments = comments + "</ul></li></ul>";
                    comments_roster[repo["repo_name"]] = comments;

                    items.push('<li class="list-group-item"><div class="row">'

                                // repo_owner/repo_name (link to repo on GitHub)
                                + '<div class="col-md-5">'
                                + '<a href="' + repo["repo_url"] + '">'
                                + repo["repo_owner"] + '/' + repo["repo_name"]
                                + '</a>'
                                + '</div>'

                                // X PRs
                                + '<div class="col-md-3">'
                                + repo["pull_requests"].length + ' PRs'
                                + '</div>'

                                // X comments (button)
                                + '<div class="col-md-4"><button class="btn btn-primary sidebar-comments" id="' + repo["repo_name"] + '-comments-sidebar"">'
                                + repo["comments"].length + ' comments</button></div>'
                                + '</div></li>');

                });  // close each()

                $('#repo-roster').append(items.join(''));

                for (var i = 0; i < repos_to_monitor.length; i++) {
                    $("#"+repos_to_monitor[i]["repo"]+"-comments-sidebar").click(function(ev) {
                      var repo_name = ev.currentTarget.id.split('-')[0]
                      $("#content-title").html(repo_name + " comments")
                      $("#comments-content").hide();
                      $("#comments-content").html(comments_roster[repo_name]);
                      $('.hidden').toggleClass('hidden show');
                      $("#comments-content").slideDown();
                    });
                };

            }
        });
    }
});