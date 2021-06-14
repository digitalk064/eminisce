$(document).ready(function() {
    load_loans_list();
});

function load_loans_list()
{
    var loans_item_original = $("#loans_list_item");
    //For each item ...
    var loans_list_item = loans_item_original.clone();
    loans_list_item.find("#loans_list_item_book_title").html("Dynamically added title");
    loans_list_item.find("#loans_list_item_book_author").html("Dynamically added authors");
    $("#loans_list").append(loans_list_item);

    //Remove the original template
    loans_item_original.remove();
}