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
