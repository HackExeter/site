(function() {
  window.onload = function() {
    var inputs, members;
    inputs = [document.getElementById('initialmember')];
    members = document.getElementById('memberslist');
    document.getElementById('addmember').addEventListener('click', function(event) {
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
    return document.getElementById('signup').addEventListener('click', function(event) {
      var input;
      return $.ajax({
        url: '/register',
        data: {
          'name': document.getElementById('name').value,
          'email': document.getElementById('email').value,
          'organisation': document.getElementById('organisation').value,
          'members': JSON.stringify((function() {
            var _i, _len, _results;
            _results = [];
            for (_i = 0, _len = inputs.length; _i < _len; _i++) {
              input = inputs[_i];
              _results.push(input.value);
            }
            return _results;
          })())
        },
        success: function() {
          return location.href = 'index.html';
        }
      });
    });
  };

}).call(this);
