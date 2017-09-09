var controller = new Vue({
  el: "#controller",

  data: {
    relays: [],
    pid: [],
    sv: ''
  },

  methods: {
    loadData() {
      axios.get("/relays").then(response => this.relays = response.data);
      axios.get("/pid").then(response => this.pid = response.data);
    },

    setRelay() {
      // State is set to name field since js is retarded
      axios.post('/setRelay', {
        relayName: event.srcElement.id,
        state: event.srcElement.name
      })
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    allRelaysOff() {
      axios.post("/allRelaysOff", {
        "allRelaysOff": true
      })
        .then(function (response) {
          console.log(response)
        })
        .catch(function (error) {
          console.log(error)
        })
    },

    toggleRims() {
      axios.post("/toggleRims", {
        "state": this.pid['pid_running']
      })
        .then(function (response) {
          console.log(response)
        })
        .catch(function (error) {
          console.log(error)
        })
    },

    setSv() {
      if (this.sv > 999.9) {
        alert("Setpoint value must be less than 999.9")
      } else {
        axios.post("/setSv", {
          sv: this.sv
        })
        .then(function (response) {
          console.log(response)
        })
        .catch(function (error) {
          console.log(error)
        })
      }
      this.sv = ''
    }
  },

  mounted() {
    this.loadData();

    setInterval(function () {
      this.loadData();
    }.bind(this), 800);
  },

})
