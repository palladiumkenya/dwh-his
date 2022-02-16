
$(document).ready(function() {
        // on page load, do the following

         $.getJSON('http://127.0.0.1:8000/facilities/get_partners_list', function(data) {
            localStorage.setItem('sdp_agencies', JSON.stringify(data)); //store a key/value
         });

         $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:8000/facilities/sub_counties',
            success: function (data) {
                console.log(data)
                localStorage.setItem('subcounties', JSON.stringify(data)); //store a key/value

                /*var retrievedsubcounty = localStorage.getItem('subcounties');
                $.each( JSON.parse(retrievedsubcounty) , function(index, item) {
                  console.log(item);
                });*/
            }
         });
         $("#id_county").trigger("change");
         $("#id_partner").trigger("change");

         // if il or hts or ct was saved in DB, slide down divs containing their info
         if ($("#id_IL").is(":checked")) {
             $("#IL_info").slideDown();
            $('input[name="ushauri"]:first').prop("disabled", true);
            $('input[name="mlab"]:first').prop("disabled", true);
            $('input[name="c4c"]:first').prop("disabled", true);
        }
        if ($("#id_CT").is(":checked")) {
            $("#EMR_info").slideDown();
        }

        if ($("#id_HTS").is(":checked")) {
            $("#HTS_info").slideDown();
        }
});

$("h5").click(function(){
    var section = $(this).attr('id').split('_');
    $("#"+section).slideToggle();
});


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
        $('input[name="ushauri"]:first').prop('checked', false);
        $('input[name="mlab"]:first').prop('checked', false);
        $('input[name="c4c"]:first').prop('checked', false);
        // disable buttons
        $('input[name="ushauri"]:first').prop("disabled", true);
        $('input[name="mlab"]:first').prop("disabled", true);
        $('input[name="c4c"]:first').prop("disabled", true);
    }else{
        // uncheck check fields
        $('#IL_info input[name="ushauri"]').prop('checked', false);
        $('#IL_info input[name="mlab"]').prop('checked', false);
        $('#IL_info input[name="c4c"]').prop('checked', false);
        // enable check fields
       $('input[name="ushauri"]:first').prop("disabled", false);
       $('input[name="mlab"]:first').prop("disabled", false);
       $('input[name="c4c"]:first').prop("disabled", false);
    }
});
