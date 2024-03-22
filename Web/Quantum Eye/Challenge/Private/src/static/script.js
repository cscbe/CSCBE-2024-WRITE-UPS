async function getScreenshot(url) {
  try {
    await $('#screenshot').attr('src', '/static/loading.gif');

    const response = await fetch('/quantum-eye', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: url })
    });

    const data = await response.json();

    if (data.error) {
      $('#screenshot').attr('src', '/static/placeholder.png');
      alert(data.error);
    }

    if (data.image) {
      $('#screenshot').attr('src', 'data:image/jpeg;base64,' + data.image);
    }
    
  } catch (error) {
    console.error(error);
    $('#screenshot').attr('src', 'data:image/jpeg;base64,' + data.image);
    alert('There was an error while getting the screenshot. If this problem persists, contact an admin.');
  }
}

$(document).ready(function() {
  $('#urlForm').on('submit', function(event) {
    event.preventDefault();
    const url = $('#url').val();
    getScreenshot(url);
  });
})
