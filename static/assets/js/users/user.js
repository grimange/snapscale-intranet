//Author: RA
//Purpose: Users Main JS class
//Date: 5/16/2025

import {IntranetGlobal} from "../global/main.js";

export class User extends IntranetGlobal {
    constructor(){
        super()
        this.noProfileResult = $("#noProfileResult")
        this.employeeUpdateForm = $("#employeeForm")
    }

    link_profile(employeeId) {
        $.ajax({type: "POST", url: this.user_profile_url, dataType:'json',
            data: {'csrfmiddlewaretoken': this.csrftoken, 'employeeId': employeeId, 'action': 'link_profile'},
            beforeSend: function(){

            },
            success: function(response){
                location.reload()
            },
            error: function(response){
                console.log(response)
                Swal.fire({title: "Error", text: response.responseJSON.message, icon: "error"})
            }
        })
    }
    load_no_result(response) {
        const self = this
        const ul = $('<ul class="list-group m-1"></ul>')
        ul.append(`<li class="list-group-item border-primary">
            <i class="icofont icofont-arrow-right"></i> <span class="badge badge-info">Name </span> ${response.name}</li>`)
        ul.append(`<li class="list-group-item border-primary">
            <i class="icofont icofont-arrow-right"></i><span class="badge badge-info">Start Date </span> ${response.start_date}</li>`)
        ul.append(`<li class="list-group-item border-primary">
            <i class="icofont icofont-arrow-right"></i> <span class="badge badge-info">Birth Date </span> ${response.birth_date}</li>`)

        this.noProfileResult.empty().append(ul)
        this.noProfileResult.append('<div class="text-end"><button class="btn btn-primary" id="btnLinkProfile">LINK</button></div>')

        $("#btnLinkProfile").off('click').on("click", function(){
            Swal.fire({
            title: "Are you sure?",
            text: "You want to link this profile to your account?",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#16C7F9",
            cancelButtonColor: "#FC4438",
            confirmButtonText: "Yes",
        }).then((result) => {
            if (result.isConfirmed) {
                self.link_profile(response.employeeId)
            }
        })
        })
    }
    load_no_profile(){
        const self = this

        $("#noProfileSavePartButton").on("click", function(){
            const submit = $(this)
            const profileId = $("#profileId")

            if(profileId.val().length < 5){
                profileId.addClass("is-invalid").select().focus()
                return false
            }
            else {
                profileId.removeClass("is-invalid")
                profileId.addClass("is-valid")
            }

            $.ajax({type: "POST", url: self.user_profile_url, dataType:'json',
                data: {'csrfmiddlewaretoken': self.csrftoken, 'employeeId': profileId.val(), 'action': 'get_profile'},
                beforeSend: function(){
                    profileId.prop("disabled", true)
                    submit.prop("disabled", true)
                    submit.html('Checking <i class="fa-solid fa-spinner fa-spin-pulse"></i>')
                },
                success: function(response){
                    profileId.removeClass("is-valid")
                    profileId.prop("disabled", false)
                    profileId.select()
                    submit.prop("disabled", false)
                    submit.html('Submit')

                    self.load_no_result(response)
                },
                error: function(response){
                    profileId.removeClass("is-valid")
                    profileId.prop("disabled", false)
                    profileId.select().focus()
                    submit.prop("disabled", false)
                    submit.html('Submit')

                    self.noProfileResult.empty().html('<div class="col-md-3 alert alert-danger">' + response.responseJSON.message + '</div>')
                }
            })
        })
    }
    load_update_profile(){
        const self = this
        const submit = $("#employeeFormSubmit")

        self.employeeUpdateForm.off('submit').on("submit", function(e){
            e.preventDefault()
            const form = $(this)
            const formDataArray = form.serializeArray();
            const formDataObj = {}

            formDataArray.forEach(function (item) {
              // If a field name appears multiple times, convert to array
              if (formDataObj[item.name]) {
                if (Array.isArray(formDataObj[item.name])) {
                  formDataObj[item.name].push(item.value);
                } else {
                  formDataObj[item.name] = [formDataObj[item.name], item.value];
                }
              } else {
                formDataObj[item.name] = item.value;
              }
            })

            formDataObj['action'] = 'update_profile'
            formDataObj['csrfmiddlewaretoken'] = self.csrftoken

            $.ajax({type: "POST", url: self.user_profile_url, data:formDataObj, dataType:'json',
                beforeSend: function(){
                    submit.prop("disabled", true)
                    submit.html('Updating <i class="fa-solid fa-spinner fa-spin-pulse"></i>')
                },
                success: function(response){
                    submit.prop("disabled", false)
                    submit.html('Update')

                },
                error: function(response){
                    console.log(response)
                    submit.prop("disabled", false)
                    submit.html('Update')
                }
            })

        })
    }
}
