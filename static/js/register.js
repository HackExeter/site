(function() {
  // Open or close registration
  if (new Date() > 1427169600000) {

    // Open registration
    $('#real-registration').show()
    var inputs, members;
    inputs = [document.getElementById('initialmember')];
    members = document.getElementById('memberslist');
    $('#addmember').on('click', function(event) {
      var newDiv, newInput;
      newDiv = document.createElement('div');
      newInput = document.createElement('input');
      newInput.type = 'name';
      newInput.className = 'form-control';
      newInput.placeholder = 'Jane Smith';
      newDiv.appendChild(newInput);
      members.appendChild(newDiv);
      return inputs.push(newInput);
    });
    $('#signup').on('click', function(event) {
      var input;
      $.ajax({
        url: '/register',
        data: {
          'name': $('#name').val(),
          'email': $('#email').val(),
          'organisation': $('#organisation').val(),
          'members': JSON.stringify(inputs.map(function(x) { return x.value; }))
        },
        success: function() {
          // Redirect
          location.href = '/';
        }
      });
    });

  } else {

    // Pre-registration
    $('#pre-registration').show()
    $('#interest-signup').on('click', function(event) {
      $.ajax({
        url: '/interested',
        data: {
          'email': $('#interest-email').val()
        },
        success: function() {
          // Redirect
          location.href = '/';
        }
      });
    });
  }

}).call(this);
