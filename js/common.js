var darkThemeBool = false;

      async function sleep() {
        console.log("sleeping");
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      async function darkTheme() {
        if(darkThemeBool) {
          document.body.style.backgroundColor = "white";
          document.body.style.color = "black";
          document.getElementById("darkTheme").innerHTML = "<i class='bi bi-moon-fill'></i>";
          darkThemeBool = false;
        } else {
          document.body.style.backgroundColor = "black";
          document.body.style.color = "white";
          document.getElementById("darkTheme").innerHTML = "<i class='bi bi-sun-fill'></i>";
          darkThemeBool = true;
        }
      }
      let darkThemeBtn = document.getElementById("darkTheme");
      darkThemeBtn.addEventListener("click", darkTheme);
     