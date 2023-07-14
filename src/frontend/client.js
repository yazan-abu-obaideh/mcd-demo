    // Function to retrieve the header content from the API
    function getHeaderContent() {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", "http://localhost:5000/health", true);
        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4 && xhr.status === 200) {
            const headerContent = xhr.responseText;
            document.getElementById("header").innerText = headerContent;
          }
        };
        xhr.send();
      }
      function optimizeBike() {
        let url = "http://localhost:5000/optimize";
        const requestBody =  {
        "seed-bike": {
            "seat_x": -9,
            "seat_y": 27,
            "handle_bar_x": 16.5,
            "handle_bar_y": 25.5,
            "crank_length": 7
        },
        "body-dimensions": {"height": 75, "sh_height": 61.09855828510818, "hip_to_ankle": 31.167514055725047,
                               "hip_to_knee": 15.196207871637029, "shoulder_to_wrist": 13.538605228960089,
                               "arm_len": 16.538605228960087, "tor_len": 26.931044229383136,
                               "low_leg": 18.971306184088018, "up_leg": 15.196207871637029}
  };
  
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(requestBody)
    })
    .then(function(response) {
      if (response.ok) {
      let resText = response.text();
      document.getElementById("optimizationResponse").innerText = resText;
        return resText;
      }
      throw new Error("Request failed with status: " + response.status);
    })
    .then(function(headerContent) {
      document.getElementById("header").innerText = headerContent;
    })
    .catch(function(error) {
      console.log(error);
    });
  
  
  
      }
  