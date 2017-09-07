// var recipe = new Vue({
//   el: "#body",
//   delimiters: ["[[", "]]"],
//   data: {
//     selected: '1',
//   }
// })

var controller = new Vue({
  el: "#controller",
  methods: {
    toggleRelay(event) {
      // r/badcode
      axios.post('/toggleRelay', {
        relayName: event.srcElement.id.replace("-button", ''),
        status: event.srcElement.classList.toString().includes("is-info")
      })
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }
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
