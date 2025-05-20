//Author: RA
//Purpose: Main Js for Employee List
//Date: 5/20/2025

$(document).ready(function(){
    $("#employeesTable").DataTable({
        lengthChange: false,
        pageLength: 25
    });
})
