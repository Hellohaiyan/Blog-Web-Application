$('#comment-form').submit(function(e){
    e.preventDefault();
    var serializedData = $(this).serialize();

  if(! serializedData === ""){
    $("#alert-comment-msg").text("Comment cannot be blank").removeClass("d-none");
    return;
  }

    $.ajax({
        type: 'POST',
        url: add_comment_url,
        data: serializedData,
        success: function (response) {

            $("#comment-form").trigger('reset');

            $('#commentTextAarea').focus();

            var comment = JSON.parse(response["comment"]);
            var fields = comment[0]["fields"];

            var user = JSON.parse(response["user"]);
            var comment_id = JSON.parse(response["id"]);

            $("#comment-area").prepend(
                `
                <div class="d-flex pt-2" id="comment-${comment_id}-div-area">
                  <div class="comment-image">
                    <img width="30px" height="30px" class="img-fluid rounded-circle"
                         src="${avatar}">
                    </div>
                    <div class="comment-text">
                      <h5 class="comment-name ps-2"><a href="{% url 'profile' request.user %}">${user.name}</a></h5>
                      <p id="comment-${comment_id}" class="card-text ps-2">${fields["comment"]||""}</p>
                      <p class="card-text ps-2">
                        <small id="comment-${comment_id}-updated_at"  class="text-muted">Last updated: ${fields["updated_at"]||""}</small>
                        <span>
                          <img data-comment="comment-${comment_id}" id="comment-${comment_id}-edit-icon" class="edit-comment-icon" style="cursor: pointer;" width="20px" height="20px" src="${edit}">
                          <img data-comment="comment-${comment_id}" data-id ="${comment_id}" data-comment="comment-${comment_id}" id="comment-${comment_id}-save-icon" class="save-comment-icon d-none" style="cursor: pointer;" width="20px" height="20px" src="${save}">
                          <img data-comment="comment-${comment_id}" data-id ="${comment_id}" id="comment-${comment_id}-close-icon" class="close-comment-icon d-none" style="cursor: pointer;" width="20px" height="20px" src="${close}">
                          <img data-comment="comment-${comment_id}" id="comment-${comment_id}-delete-comment-icon" class="delete-comment-icon" style="cursor: pointer;" width="20px" height="20px" src="${trash}">
                          <span id="comment-${comment_id}-confirm-comment-delete" class="d-none">
                            Are you sure?
                            <button data-id="${comment_id}" id="comment-${comment_id}-delete-comment-button" data-comment="comment-${comment_id}" type="button" class="btn btn-danger btn-sm delete-comment-button">Yes</button>
                            <button id="comment-${comment_id}-cancel-delete-comment-button" data-comment="comment-${comment_id}" type="button" class="btn btn-secondary btn-sm cancel-delete-comment-button">Cancel</button>
                          </span>
                        </span>
                      </p>
                    </div>
                </div>
                <hr id="comment-${comment_id}-hr">
                `
            )
        },
        error: function (response) {
            var err_msg = response["responseJSON"]["error"]
            $("#alert-comment-msg").text(err_msg).removeClass("d-none");
        }
    })
});



$("span").on("click", "img.edit-comment-icon", function(){
  var comment = $(this).attr("data-comment");
  $("#"+comment).prop('contenteditable', 'true').addClass("edit-element").focus();
  $(this).addClass("d-none");
  $("#"+comment+"-close-icon").removeClass("d-none");
  $("#"+comment+"-save-icon").removeClass("d-none");
});



$("span").on("click", "img.close-comment-icon", function(){
  var comment_id_attr = $(this).attr("data-comment");

  var comment_id = $(this).attr("data-id");

  edit_comment_url = edit_comment_url.replace(/1234/, comment_id.toString())
  $.ajax({
    type: 'GET',
    url: edit_comment_url,
    headers: {
      'Content-Type':'application/json',
      'X-CSRFToken': csrftoken
    },
    success: function (response) {
      $("#comment-"+comment_id).text(response.comment)
      $("#"+comment_id_attr).prop('contenteditable', 'false').removeClass("edit-element");
      $("#"+comment_id_attr+"-close-icon").addClass("d-none");
      $("#"+comment_id_attr+"-save-icon").addClass("d-none");
      $("#"+comment_id_attr+"-edit-icon").removeClass("d-none");

    },
    error: function (response) {
        var err_msg = response["responseJSON"]["error"]
        $("#alert-comment-msg").text(err_msg).removeClass("d-none");
     }
  })

  return false;

});


$("span").on("click", "img.save-comment-icon", function(){
  var comment_id_attr = $(this).attr("data-comment");

  var comment = $("#"+comment_id_attr).text();
  var comment_id = $(this).attr("data-id");

  var article_slug = $(this).attr("data-slug");


  if(comment === ""){
    $("#alert-comment-msg").text("Comment cannot be blank").removeClass("d-none");
    return;
  }

  edit_comment_url = edit_comment_url.replace(/1234/, comment_id.toString())

  $.ajax({
    type: 'PUT',
    url: edit_comment_url,
    headers: {
      'Content-Type':'application/json',
      'X-CSRFToken': csrftoken
    },
    data: JSON.stringify({'comment': comment}),
    success: function (response) {
      let date = new Date(Date.parse(response.updated_at));
      $("#comment-"+comment_id+"-updated_at").text("Last updated: " + date.toUTCString());
      $("#comment-"+comment_id).text(comment)

      $("#"+comment_id_attr).prop('contenteditable', 'false').removeClass("edit-element");
      $("#"+comment_id_attr+"-close-icon").addClass("d-none");
      $("#"+comment_id_attr+"-save-icon").addClass("d-none");
      $("#"+comment_id_attr+"-edit-icon").removeClass("d-none");

    },
    error: function (response) {
        var err_msg = response["responseJSON"]["error"]
        $("#alert-comment-msg").text(err_msg).removeClass("d-none");
     }
  })

});



$("span").on("click", "img.delete-comment-icon", function(){
  var comment = $(this).attr("data-comment");
  $(this).addClass("d-none");
  $("#"+comment+"-confirm-comment-delete").removeClass("d-none");
  return false;
});


$("span").on("click", "button.cancel-delete-comment-button", function(){

  var comment = $(this).attr("data-comment");
  $("#"+comment+"-confirm-comment-delete").addClass("d-none");
  $("#"+comment+"-delete-comment-icon").removeClass("d-none");
  return false;
});


$("span").on("click", "button.delete-comment-button", function(){

  delete_comment_url_modified = delete_comment_url

  var comment = $(this).attr("data-comment");
  var comment_id = $(this).attr("data-id");

  delete_comment_url_ajax = delete_comment_url_modified.replace(/1234/, comment_id.toString())

  $.ajax({
    type: 'DELETE',
    url: delete_comment_url_ajax,
    headers: {
      'Content-Type':'application/json',
      'X-CSRFToken': csrftoken
    },
    success: function (response) {
      $("#"+comment+"-div-area").remove();
      $("#"+comment+"-hr").remove();
    },
    error: function (response) {
        var err_msg = response["responseJSON"]["error"]
        $("#alert-comment-msg").text(err_msg).removeClass("d-none");
     }
  })

  return false;
});
