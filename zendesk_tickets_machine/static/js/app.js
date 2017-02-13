/*!
 * Zendesk Ticket Machine Custom Javascript
 * Copyright 2017 Pronto Group
 * Licensed under Pronto Tools
 */
function check_ticket_type() {
  var ticket_type_list = document.getElementById('id_ticket_type');
  var due_at = document.getElementById('due_at');
  var selected_ticket_type = ticket_type_list.options[ticket_type_list.selectedIndex].value;

  if(selected_ticket_type == 'task') {
    due_at.style.display = 'block';
  }
  else {
    due_at.style.display = 'none';
  }
}

$(document).ready(check_ticket_type());

$(function() {
    $("#datepicker").datepicker();
});

$(function() {
    $("#edit_due_at").datepicker();
});

/* select all*/
$(':checkbox[name=select_all]').click (function () {
  $(':checkbox[name=check]').prop('checked', this.checked);
});

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$("#button_edit_once_form").click(function(event){
    var id_list = edit_once();
    $.ajax({
         type:"POST",
         url:"/edit_once/",
         data: {
                  'id_list[]': id_list,
                  'edit_tags': $('#edit_tags').val(),
                  'edit_subject': $('#edit_subject').val(),
                  'edit_due_at': $('#edit_due_at').val(),
                  'edit_assignee': $('#edit_assignee').val()
                },
        success: location.reload()
    });
});

function edit_once(){
  items = $(':checkbox[name="check"]:checked');
  var id_list = [];
  for(i = 0; i<items.length; i++){
    id_list.push(items[i].value);
  }
  return id_list;
}
