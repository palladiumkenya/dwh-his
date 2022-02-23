
$(document).ready(function() {
        // on page load, do the following
        if (disable_fields === true){
            $('#facility_form :input').prop("disabled",true);
        }

         $.getJSON('http://127.0.0.1:8000/facilities/get_partners_list', function(data) {
            localStorage.setItem('sdp_agencies', JSON.stringify(data)); //store a key/value
         });

         //   url: 'http://127.0.0.1:8000/facilities/sub_counties',
         $.getJSON('http://127.0.0.1:8000/facilities/sub_counties', function(data) {
                console.log(data)
                localStorage.setItem('subcounties', JSON.stringify(data)); //store a key/value
         });

         //$("#id_county").val("36").change();
         $("#id_county").trigger("change");
         $("#id_partner").trigger("change");

         setTimeout(function() {
             $("#id_county").trigger("change");
            //$("#id_sub_county").val("30").trigger("change");
            $("#id_sub_county").val(String(subcounty_id_saved));
        }, 2000);

         // if il or hts or ct was saved in DB, slide down divs containing their info
         if ($("#id_IL").is(":checked")) {
             $("#IL_info").slideDown();
            // $('input[name="ushauri"]:first').prop("disabled", true);
            // $('input[name="mlab"]:first').prop("disabled", true);
            // $('input[name="c4c"]:first').prop("disabled", true);
             $('#MHealth_info input[name="ushauri"]').prop("disabled", true);
             $('#MHealth_info input[name="mlab"]').prop("disabled", true);
             $('#MHealth_info input[name="c4c"]').prop("disabled", true);
        }else{
             //$('#IL_info input[name="mlab"]').val(mlab);
             $('#IL_info input[name="mlab"]').prop('checked', false);
             $('#IL_info input[name="ushauri"]').prop('checked', false);
             $('#IL_info input[name="c4c"]').prop('checked', false);
         }
        if ($("#id_CT").is(":checked")) {
            $("#EMR_info").slideDown();
        }

        if ($("#id_HTS").is(":checked")) {
            $("#HTS_info").slideDown();
        }
        console.log("testing");
        console.log($('#MHealth_info input[name="ushauri"]').val());
});


//var section = $(this).attr('id').split('_');



$("#id_county").change(function(){
  var retrievedsubcounty = localStorage.getItem('subcounties');

    var value = $("#id_county").val();

    $.each( JSON.parse(retrievedsubcounty) , function(index, item) {

       if(item["county"] === parseInt(value)){
             $("#id_sub_county").empty();
            if(item["sub_county"].length > 0){
                $.each( item["sub_county"] , function(sub_ind, sub_item) {
                    $('#id_sub_county').append("<option value="+sub_item['id']+">"+sub_item['name']+"</option>");
                });
            }
       }
    });
});

$("#id_partner").change(function(){
  var retrievedsdp_agencies = localStorage.getItem('sdp_agencies');

    var value = $("#id_partner").val();

    $.each( JSON.parse(retrievedsdp_agencies) , function(index, item) {

       if(item["partner"] === parseInt(value)){
             $("#id_agency").val(item['agency']['name']);
       }
    });
});


$("#id_CT").click(function(){
    $("#EMR_info").slideToggle();
});

$("#id_HTS").click(function(){
    $("#HTS_info").slideToggle();
});

$("#id_IL").click(function(){
    $("#IL_info").slideToggle();
    //$('input[name="ushauri"]').prop("disabled", true);
    if ($("#id_IL").is(":checked")) {
        // uncheck buttons
        // $('#MHealth_info input[name="ushauri"]').prop('checked', false);
        // $('#MHealth_info input[name="mlab"]').prop('checked', false);
        // $('#MHealth_info input[name="c4c"]').prop('checked', false);
        // disable buttons
        console.log("knowing");
        console.log($('#MHealth_info input[name="ushauri"]').val());
        $('#MHealth_info input[name="ushauri"]').prop("disabled", true);
        $('#MHealth_info input[name="mlab"]').prop("disabled", true);
        $('#MHealth_info input[name="c4c"]').prop("disabled", true);
        // // set the values
        if ($('#MHealth_info input[name="ushauri"]').is(":checked")) {
            $('#IL_info input[name="ushauri"]').prop('checked', true);
        }
        if ($('#MHealth_info input[name="mlab"]').is(":checked")) {
            $('#IL_info input[name="mlab"]').prop('checked', true);
        }
        if ($('#MHealth_info input[name="c4c"]').is(":checked")) {
            $('#IL_info input[name="c4c"]').prop('checked', true);
        }
        // $('#IL_info input[name="ushauri"]').val(ushauri);
        // $('#IL_info input[name="mlab"]').val(mlab);
        // $('#IL_info input[name="c4c"]').val(c4c);
    }else{
        // uncheck check fields
        $('#IL_info input[name="ushauri"]').prop('checked', false);
        $('#IL_info input[name="mlab"]').prop('checked', false);
        $('#IL_info input[name="c4c"]').prop('checked', false);
        // enable check fields
        $('#MHealth_info input[name="ushauri"]').prop("disabled", false);
        $('#MHealth_info input[name="mlab"]').prop("disabled", false);
        $('#MHealth_info input[name="c4c"]').prop("disabled", false);
    }
});
