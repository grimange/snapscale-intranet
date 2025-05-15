//Author: RA
//Purpose: Global JS
//Date: 5/16/2025

export class IntranetGlobal {
  constructor() {
      this.csrftoken = $("meta[name='csrf-token']").attr("content")
      this.user_profile_url = window.location.origin + "/users/profile/"
  }
}
