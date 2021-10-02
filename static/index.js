//Hide navbar links
document.addEventListener('DOMContentLoaded', function () {

    const navCollapse = document.querySelector('.navbar-collapse')
    const allNavLinks = document.querySelectorAll('.link-hide')

    allNavLinks.forEach(item => item.addEventListener("click", () => navCollapse.classList.remove('show')))
    })

//Datepicker
$(function() {
$('.input-daterange').datepicker({
    format: "dd/mm/yy",
    weekStart: 1,
    language: "pl",
    orientation:"top auto",
    daysOfWeekDisabled: "0,6",
    todayHighlight: true
    });

//    $('.input-daterange').on('apply.datepicker', function(ev, picker) {
//        $('#numberdays').val(picker.endDate.diff(picker.startDate, "days"));
//    });
});

$('.datepicker').datepicker({
    format: "dd/mm/yy",
    weekStart: 1,
    language: "pl",
    orientation: "top auto",
    daysOfWeekDisabled: "1,2,3,4,5",
    todayHighlight: true,
});

//Numbering automatically rows in tables
function addRowCount(tableAttr) {
  $(tableAttr).each(function(){
    $('th:first-child, thead td:first-child', this).each(function(){
      var tag = $(this).prop('tagName');
      $(this).before('<'+tag+'>Lp.</'+tag+'>');
    });
    $('td:first-child', this).each(function(i){
      $(this).before('<td>'+(i+1)+'.</td>');
    });
  });
}
addRowCount('.js-serial');

//Requests options
$('input[type="radio"]').click(function(){
     if($(this).attr("value")=="W"){
            $(".Box").show('slow');
           $(".Box2").hide('slow');
        }
        if($(this).attr("value")=="WS"){
            $(".Box").hide('slow');
            $(".Box2").show('slow');
        }
        if($(this).attr("value")=="WN"){
            $(".Box").hide('slow');
            $(".Box2").show('slow');
        }
           if($(this).attr("value")=="DW"){
            $(".Box").hide('slow');
            $(".Box2").hide('slow');
        }
    });
$('input[type="radio"]').trigger('click');

//Tables search
$(document).ready(function(){
  $("#myInput1").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable1 tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
    $("#myTable3 tr td").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

function search() {

  const input = document.getElementById("myInput");
  const filter = input.value.toUpperCase();
  const table = document.querySelector(".myTable");
  const tr = table.getElementsByTagName("tr");
  let td, txtValue;

  for (let i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[2];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function search2() {

  const input = document.getElementById("myInput2");
  const filter = input.value.toUpperCase();
  const table = document.querySelector(".myTable2");
  const tr = table.getElementsByTagName("tr");
  let td, txtValue;

  for (let i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[2];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

