function initView()
{
    $("#id_start_date, #id_end_date").blur( (function () {
        if($("#id_start_date").val() != "" &&  $("#id_end_date").val() != "")
          $("#use_form").submit();
    }));
    $("#id_r_id").val($("#room_id").text());
    $("#use_form").on('submit', function (e) {
        e.preventDefault();
        $.ajax({
          type: 'post',
          url: '/admin_view_room_usage/',
          data: $('#use_form').serialize(),
          
          success: function(result) {
            //Clean up table first
            $("#results_table tbody").empty();
            bookings = result["bookings"];

            if(bookings.length == 0)
              $("#results_table tbody").append('<p>No result</p>');

            for (var b in bookings) //b is index, not the actual object
            {
              addToTable($("#results_table tbody"), bookings[b]);
            }
          },
  
          fail: function ()
          {
            $("#results_table tbody").html('<p>Cannot connect to server. Please retry.</p>');
          },
          error: function()
          {
            $("#results_table tbody").html('<p>Your search criteria were invalid! Please check your date format.</p>');
          }
        });
      })
}

function addToTable(table, data)
{
    //Black magic to display in proper format
    var start_date = new Date(data['start']).toJSON().slice(0,10).split('-').reverse().join('/') + ' ' + new Date(data['start']).toLocaleTimeString();
    var end_date = new Date(data['end']).toJSON().slice(0,10).split('-').reverse().join('/') + ' ' + new Date(data['end']).toLocaleTimeString();
    table.append('<tr> <td style = "height: 50px; text-align: left;">' 
    + '<div style = "float: left;">'
    + 'Start: <b>' + start_date + '</b><br>'
    + 'End: <b>' + end_date + '</b><br>'
    + '</div>' 
    + '<div style = "float: right;">'
    + 'Booker: ' + '<b>' + data["booker_name"] + '</b>'
    + '</div>'
    + '</td></tr>'
    );
}

function rowHTML(data)
{
    var html;
    if(data["available"])
        var status_html = '✅ <span style = "color:green">Available</span>'
    else
        var status_html = '❌ <span style = "color:red">Unavailable</span>'
    html =  '<b>'+data["name"] + '</b>' + '<br>'
            + "🏢 "+ data["location"] + '<br>'
            + "Capacity: " + data["capacity"] + '<br>' 
            + status_html + '<br>'
            + '$ ' + data["price"] + ' / hour' + '<br>'
    return html;
}

function makeClickable()
{
    //Just hardcode the element id...
    $("#results_table tbody tr").click(function(){
        var row_index = $(this).index();
        handleBookRoom(row_index);
    });
}

function handleBookRoom(index) //Populate information in the modal
{
    if(!rooms[index]["available"])
    {
        alert("This room is occupied");
        return;
    }
    var date =  $("#id_date").val();
    var start_time = $("#id_start_time").val();
    var duration = parseInt($("#id_duration").val());
    var end_time = calcEndTime(start_time, duration);
    var price = rooms[index]["price"] * duration;
    hookBookFunction(rooms[index]["id"],date,start_time,duration,price);

    $("#bookmodal_desc").html("");
    $("#bookmodal_desc").append("Room: <b>" + rooms[index]["name"] + "<br>");
    $("#bookmodal_desc").append("Location: <b>" + rooms[index]["location"] + "</b></p>");
    $("#bookmodal_desc").append("<p>From: <b>" + date + " " + start_time + "</b>");
    
    $("#bookmodal_desc").append("<p>To: <b>" + date + " " 
                + end_time + "</b></p>");
    $("#bookmodal_price_total").text(price);

    $("#book_modal").modal();
}

function hookBookFunction(id, date, start_time, duration, price)
{
    $("#accept_book").off('click');
    $("#accept_book").click( function () {
        if(bookings.length >= 3)
        {
            alert("You can only have a maximum of 3 bookings");
            return;
        }
        console.log("Book data: " + id + ' ' + date + ' ' + start_time + ' ' +  duration + ' ' + price);

        //Fill the hidden form first
        $("#id_b_room_id").val(id);
        $("#id_b_date").val(date);
        $("#id_b_start_time").val(start_time);
        $("#id_b_duration").val(duration);
        $("#id_b_price").val(price);

        $.ajax({
            type: 'post',
            url: 'book_room',
            data: $('#book_form').serialize(),
            
            success: function(result) {
                console.log(result);
                handleBookSuccess();
            },
    
            fail: function ()
            {
              alert ("There was an error connecting to the server! Please retry")
            },
            error: function(result)
            {
              alert (result.responseJSON.msg);
            }
          });
    });
}

function handleBookSuccess()
{
    //Close current modal and open success modal
    $("#book_modal").modal('toggle');
    $("#book_success_modal").modal();

    //Refresh lists
    getUpcoming(); //Auto get upcoming  bookings
    $("#search_form").submit(); //Auto refresh room list
}

function calcEndTime(start, duration)
{
    var new_hour = parseInt(start.substring(0,2)) + duration;
    var new_string = new_hour + ":" + start.slice(3,5);
    return new_string;
}
