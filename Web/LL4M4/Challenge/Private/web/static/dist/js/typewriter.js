const words = ["Hello, World !", "Welcome to my website !", "I am the most el33t h4ck3r"];
let i = 0;
let j = 0;
let prepend = "<-- ";
let append = " -->";
let currentWord = " ";
let isDeleting = false;

function type() {
  currentWord = words[i];
  if (isDeleting) {
    document.getElementById("typewriter").textContent = prepend + currentWord.substring(0, j-1) + append;
    j--;
    if (j == 0) {
      isDeleting = false;
      i++;
      if (i == words.length) {
        i = 0;
      }
      setTimeout(type, 1000); 
    } else {
      setTimeout(type, 100); 
    }
  } else {
    document.getElementById("typewriter").textContent = prepend + currentWord.substring(0, j+1) + append;
    j++;
    if (j == currentWord.length) {
      isDeleting = true;
      setTimeout(type, 1000); 
    } else {
      setTimeout(type, 100);
    }
  }
}
type(); 