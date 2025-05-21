//Author: RA
//Purpose: Main Class Dashboard JS
//Date: 5/22/2025

import {IntranetGlobal} from "../global/main.js";

export class Post extends IntranetGlobal{
    constructor() {
        super();
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
                data: {post_content: content.getData(),
                       csrfmiddlewaretoken: self.csrftoken,
                       action: 'new_post'
                },
                beforeSend: function () {
                    submit.attr("disabled", true)
                    submit.html("Posting <i class='fa-solid fa-spinner fa-spin-pulse'></i>")

                },
                success: function(response){
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
