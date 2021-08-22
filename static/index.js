$(function() {
$('.input-daterange').datepicker({
    format: "dd/mm/yy",
    weekStart: 1,
    language: "pl",
    orientation:"top auto",
    daysOfWeekDisabled: "0,6",
    todayHighlight: true
    });

    $('.input-daterange').on('apply.datepicker', function(ev, picker) {
        // picker.startDate and picker.endDate are already Moment.js objects.
        // You can use diff() method to calculate the day difference.
        $('#numberdays').val(picker.endDate.diff(picker.startDate, "days"));
    });
});

$('.datepicker').datepicker({
    format: "dd/mm/yy",
    weekStart: 1,
    language: "pl",
    orientation: "top auto",
    daysOfWeekDisabled: "1,2,3,4,5",
    todayHighlight: true,
});

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

// Call the function with table attr on which you want automatic serial number
addRowCount('.js-serial');


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

$(document).ready(function(){
  $("#myInput1").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable1 tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
    $("#myTable3 tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

$(document).ready(function(){
  $("#myInput2").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable2 tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
        $("#myTable4 tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

//$("#wnioski_table td:contains('None')").text("");
//$("#wnioski_table td").text(function () {
//    return $(this).text().replace("None", " ");
//});