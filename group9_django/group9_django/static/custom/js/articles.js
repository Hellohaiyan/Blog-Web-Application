$("#edit-article-icon").click(function(){
  $(this).addClass("d-none");
  $("#close-article-icon").removeClass("d-none");
  $("#save-article-icon").removeClass("d-none");
  $("#change-image").removeClass("d-none");
  $("#category-div").removeClass("d-none").addClass("edit-element");
  $("#article-cover").removeClass("d-none");
  $("#article-title").prop('contenteditable', 'true').addClass("edit-element").focus();
  $("#article-subtitle").prop('contenteditable', 'true').addClass("edit-element");
  $("#article-content").prop('contenteditable', 'true').addClass("edit-element");
});


$("#article-image-form").submit(function(e){
  e.preventDefault();
  var data = new FormData($(this)[0]);
  $.ajax({
      type: 'POST',
      url: update_article_url,
      headers: {
        'X-CSRFToken': csrftoken
      },
      data: data,
      processData: false,
      contentType: false,
      cache: false,
      success: function (response) {
        $("#article-cover-image").attr("src", response.photo);
        $('#image_modal').modal('toggle');
      },
      error: function (response) {
          var err_msg = response["responseJSON"]["error"]
          $("#alert-article-msg").text(err_msg).removeClass("d-none");
      }
  })
});

$("#save-article-icon").click(function(){
  var title = $("#article-title").text();
  var subtitle = $("#article-subtitle").text();
  var content = $("#article-content").text();
  var article_cover = $("#article-cover").val();
  var category_id = $("#select-article-category").val();
  var category = $("#select-article-category option:selected").text()

  if(title === ""){
    $("#alert-article-msg").text("Title field cannot be left blank").removeClass("d-none");
    return;
  }

  if(subtitle === ""){
    $("#alert-article-msg").text("Subtitle field cannot be left blank").removeClass("d-none");
    return;
  }

  if(content === ""){
    $("#alert-article-msg").text("Content field cannot be left blank").removeClass("d-none");
    return;
  }

  if(article_cover === ""){
    $("#alert-article-msg").text("Article_cover field cannot be left blank").removeClass("d-none");
    return;
  }
  $.ajax({
    type: 'PUT',
    url: edit_article_url,
    headers: {
      'Content-Type':'application/json',
      'X-CSRFToken': csrftoken
    },
    data: JSON.stringify({
      'title': title,
      'subtitle' : subtitle,
      'content' : content,
      'category' : category_id,
      'article_cover': article_cover
    }),
    success: function (response) {
      let date = new Date(Date.parse(response.updated_at));
      $("#article-updated-at").text("Last updated: " + date.toUTCString());
      $("#article-title").text(title);
      $("#article-subtitle").text(subtitle);
      $("#article-content").text(content);
      $("#article-category").text(category)
      $("#close-article-icon").addClass("d-none");
      $("#save-article-icon").addClass("d-none");
      $("#edit-article-icon").removeClass("d-none");
      $("#category-div").addClass("d-none");
      $("#article-cover").addClass("d-none");
      $("#change-image").addClass("d-none");

      $("#article-title").prop('contenteditable', 'false').removeClass("edit-element").focus();
      $("#article-subtitle").prop('contenteditable', 'false').removeClass("edit-element");
      $("#article-content").prop('contenteditable', 'false').removeClass("edit-element");

    },
    error: function (response) {
        var err_msg = response["responseJSON"]["error"]
        $("#alert-article-msg").text(err_msg).removeClass("d-none");
     }
  })


});

$("#close-article-icon").click(function(){

  $.ajax({
    type: 'GET',
    url: edit_article_url,
    headers: {
      'Content-Type':'application/json',
      'X-CSRFToken': csrftoken
    },
    success: function (response) {
      let date = new Date(Date.parse(response.updated_at));
      $("#article-updated-at").text("Last updated: " + date.toUTCString());
      $("#article-title").text(response.title);
      $("#article-subtitle").text(response.subtitle);
      $("#article-content").text(response.content);

      $("#close-article-icon").addClass("d-none");
      $("#save-article-icon").addClass("d-none");
      $("#edit-article-icon").removeClass("d-none");
      $("#category-div").addClass("d-none");
      $("#article-cover").addClass("d-none");
      $("#change-image").addClass("d-none");

      $("#article-title").prop('contenteditable', 'false').removeClass("edit-element").focus();
      $("#article-subtitle").prop('contenteditable', 'false').removeClass("edit-element");
      $("#article-content").prop('contenteditable', 'false').removeClass("edit-element");


    },
    error: function (response) {
        var err_msg = response["responseJSON"]["error"]
        $("#alert-article-msg").text(err_msg).removeClass("d-none");
     }
  })

  return false;

});
