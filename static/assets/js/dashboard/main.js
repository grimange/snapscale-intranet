//Author: RA
//Purpose: Dashboard Main JS
//Date: 5/22/2025
import {Post} from "./post.js";

$(document).ready(function () {
    new Post().load_new_post()
})
