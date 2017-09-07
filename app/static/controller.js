var controller = new Vue({
  el: "#controller",

  data: {
    relays: [],
    pid: []
  },

  methods: {
    loadData() {
      axios.get("/relays").then(response => this.relays = response.data);
      axios.get("/pid").then(response => this.pid = response.data);
    }
  },

  mounted() {
    this.loadData();

    setInterval(function () {
      this.loadData();
    }.bind(this), 10000);
  },

})
