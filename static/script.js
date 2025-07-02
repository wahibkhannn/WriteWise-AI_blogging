// DARK MODE TOGGLE
const toggleBtn = document.getElementById("theme-toggle-btn");

toggleBtn.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  if (document.body.classList.contains("dark-mode")) {
    toggleBtn.innerHTML = "☀️";
    localStorage.setItem("theme", "dark");
  } else {
    toggleBtn.innerHTML = "🌙";
    localStorage.setItem("theme", "light");
  }
});

// LOAD THEME PREFERENCE
window.onload = () => {
  const theme = localStorage.getItem("theme");
  if (theme === "dark") {
    document.body.classList.add("dark-mode");
    toggleBtn.innerHTML = "☀️";
  } else {
    toggleBtn.innerHTML = "🌙";
  }

  // Trigger typing animation
  typeWriter();
};

// TYPING ANIMATION (hero section heading)
const typeTarget = document.getElementById("typewriter");
const text = "WriteWise AI";
let idx = 0;

function typeWriter() {
  if (typeTarget && idx < text.length) {
    typeTarget.innerHTML += text.charAt(idx);
    idx++;
    setTimeout(typeWriter, 120);
  }
}


function generateAIContent() {
  const prompt = document.getElementById('ai_prompt').value;
  if (!prompt.trim()) {
    alert("Please enter a prompt first!");
    return;
  }


  const selectedModel = document.getElementById("model-select").value;
  

  // show the loader before making the request (api call)
  showLoader();
  fetch("/generate_ai", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      prompt: prompt,
      model: selectedModel
    })
  })
    .then(response => response.json())
    .then(data => {
      if (data.generated_content) {
        document.getElementById('content').value = data.generated_content;
      } else if (data.error) {
        alert("Error: " + data.error);
      }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("Failed to generate content.");
    })
    .finally(() => {
      //  Always hide the loader afterward
      hideLoader();
    });
}


// spinner loader
function showLoader() {
  document.getElementById("modern-loader").style.display = "flex";
}

function hideLoader() {
  document.getElementById("modern-loader").style.display = "none";
}
