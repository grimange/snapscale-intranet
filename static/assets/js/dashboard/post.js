//Author: RA
//Purpose: Main Class Dashboard JS
//Date: 5/22/2025

import {IntranetGlobal} from "../global/main.js";

export class Post extends IntranetGlobal{
    constructor() {
        super();
    }
    post_template(postId, username, post_date, content) {
        return '<div class="col-sm-12" id="post_'+ postId +'">' +
                    '<div class="card">' +
                        '<div class="card-body">' +
                            '<div class="new-users-social">' +
                                '<div class="d-flex"><img class="rounded-circle image-radius m-r-15" src="/static/assets/images/user/1.jpg" alt="">' +
                                    '<div class="flex-grow-1">' +
                                        '<h6>'+ username +'</h6>'+
                                        '<p class="c-o-light">'+ post_date +'</p>'+
                                    '</div><span class="pull-right mt-0"><i data-feather="more-vertical"></i></span>'+
                                '</div>'+
                            '</div>'+
                            '<div class="timeline-content">' +
                                content+
                                '<div class="social-chat">' +
                                '</div>'+
                                '<div class="comments-box">' +
                                    '<div class="d-flex">' +
                                        '<img class="img-50 img-fluid m-r-20 rounded-circle" alt="" src="/static/assets/images/user/1.jpg">' +
                                        '<div class="flex-grow-1">' +
                                            '<div class="input-group text-box">' +
                                                '<input class="form-control input-txt-bx" type="text" name="messageToSend_'+ postId +'" placeholder="Post your comments">'+
                                                '<div class="input-group-append">' +
                                                    '<button class="btn btn-transparent commentBtn" type="button" data-post-id="'+ postId +'">' +
                                                        '<i class="fa-regular fa-face-smile"></i>' +
                                                    '</button>'+
                                                '</div>'+
                                            '</div>'+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                            '</div>'+
                        '</div>'+
                    '</div>'+
               '</div>'
    }
    load_post(responses) {
        const self = this
        const post_wrapper = $("#dashboard-post-list")

        if(Array.isArray(responses) && responses.length > 0){
            post_wrapper.empty()
            responses.forEach(function(response){
                post_wrapper.append(self.post_template(response.id, response.username, response.post_date, response.post_content))
            })

            $('.commentBtn').off("click").on("click", function(e){
                e.preventDefault()

            })
        }
        else {
            post_wrapper.html("<h5>NO POST</h5>")
        }
    }
    load_new_post(){
        const self = this
        const submit = $("#newPostSubmit")

        submit.off("click").on("click", function(){
            const content = CKEDITOR.instances.area1

            if(content.getData() === ""){
                content.focus()
                return false
            }

            $.ajax({type: 'post', url: self.dashboard_post_url, dataType: 'json',
                data: {post_content: content.getData(), csrfmiddlewaretoken: self.csrftoken, action: 'new_post'
                },
                beforeSend: function () {
                    submit.attr("disabled", true)
                    submit.html("Posting <i class='fa-solid fa-spinner fa-spin-pulse'></i>")

                },
                success: function(response){
                    console.log(response)
                    self.load_post(response)

                    submit.attr("disabled", false)
                    submit.html("Post")
                },
                error: function(response){
                    submit.attr("disabled", false)
                    submit.html("Post")
                    console.log(response)
                }
            })
        })
    }
}
