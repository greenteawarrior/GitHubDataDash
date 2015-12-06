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
                comments_roster = {};
                // thanks http://stackoverflow.com/questions/1208467/how-to-add-items-to-a-unordered-list-ul-using-jquery
                $.each(repo_roster, function(i, repo) {
                    var comments ='<ul class="list-group">';

                    for (j=0; j < 6; j++) {
                        var current_comment = repo["comments"][j];
                        var current_comment_html = (
                             "<li class='hidden list-group-item'>"
                           + "<a href='" + current_comment["url"] + "'>"
                           + current_comment["person"]
                           + ' : '
                           + current_comment["body"]
                           + "</a></li>"
                        )
                        comments = comments + current_comment_html;
                    }
                    comments = comments + "</ul></li></ul>";
                    comments_roster[repo["repo_name"]] = comments;

                    items.push('<li class="list-group-item"><div class="row">'

                                // repo_owner/repo_name (link to repo on GitHub)
                                + '<div class="col-md-5">'
                                + '<a href="">'
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

                $("#blocks-comments-sidebar").click(function() {
                  $("#comments-content").hide();
                  $("#comments-content").html(comments_roster["blocks"]);
                  $('.hidden').toggleClass('hidden show');
                  $("#comments-content").slideDown();
                });


                $("#fuel-comments-sidebar").click(function() {
                  $("#comments-content").hide();
                  $("#comments-content").html(comments_roster["fuel"]);
                  $('.hidden').toggleClass('hidden show');
                  $("#comments-content").slideDown();
                });

                $("#blocks-examples-comments-sidebar").click(function() {
                  $("#comments-content").hide();
                  $("#comments-content").html(comments_roster["blocks-examples"]);
                  $('.hidden').toggleClass('hidden show');
                  $("#comments-content").slideDown();
                });

            }
        });
    }
});