var recipe = new Vue({
  el: "#body",
  delimiters: ["[[", "]]"],
  data: {
    selected: '1',
  }
})

$("#something").click(function(e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: "/post",
    data: {
      action: $(this).attr("value")
    }
  })
})
