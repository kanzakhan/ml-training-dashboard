/*
This file contains j-Query that performs the app's front end GUI form
validation to confirm values are what they should be, and that values are
indeed entered by the user before the form data is sent to the back-end.
This also contains the API call made to check experiment progress every 1000 ms.
*/

// Front End UI form validation
$(document).ready(function(){
    $("form[name='experiment-parms']")
      .form({
        fields: {
          experiment_name: {
            identifier: 'experiment-name',
            rules: [
              {
                type   : 'empty',
                prompt : 'Please enter the experiment name'
              }
            ]
          },
          embedding_dim: {
            identifier: 'embedding-dim',
            rules: [
              {
                type   : 'integer',
                prompt : 'Please enter a positive integer for the embedding dimensions'
              }
            ]
          },
          n_layers: {
            identifier: 'n-layers',
            rules: [
              {
                type   : 'integer',
                prompt : 'Please enter the number of layers in the RNN'
              }
            ]
          },
          hidden_size: {
            identifier: 'hidden-size',
            rules: [
              {
                type   : 'integer',
                prompt : 'Please enter a hidden size for the RNN'
              }
            ]
          },
          rnn_type: {
            identifier: 'rnn-type',
            rules: [
              {
                type   : 'empty',
                prompt : 'Please choose the RNN type'
              }
            ]
          },
          rnn_dropout: {
            identifier: 'rnn-dropout',
            rules: [
              {
                type   : 'decimal',
                prompt : 'Please enter a positive float from [0,1] for the RNN dropout probability'
              }
            ]
          },
          embedding_dropout: {
            identifier: 'embedding-dropout',
            rules: [
              {
                type   : 'decimal',
                prompt : 'Please enter a positive float from [0,1] for the embedding dropout probability'
              }
            ]
          },
          max_steps: {
            identifier: 'max-steps',
            rules: [
              {
                type   : 'integer',
                prompt : 'Please enter the number of maximum steps'
              }
            ]
          },
          iter_per_step: {
            identifier: 'iter-per-step',
            rules: [
              {
                type   : 'integer',
                prompt : 'Please enter the number of iterations per step'
              }
            ]
          },
          disable_dropout: {
            identifier: 'disable-dropout',
            rules: []
        }
        },
        onSuccess: function(event, fields) {
            event.preventDefault();
            $('#submit').addClass('disabled')
            var el = $('#experiment-form');
            $.ajax({
                type: el.attr('method'),
                url: el.attr('action'),
                data: el.serialize(),
                success: function (response) {
                    alert('Your experiment was initiated!')
                    $('#submit').removeClass('disabled')
                },
                error: function (xhr) {
                    alert(xhr.responseJSON.error)
                    $('#submit').removeClass('disabled')
                }
          });
        }
      })
    ;
    // API calls to get the progress every second
    setInterval(function() {
            $.ajax({
                type: 'get',
                url: '/progress-status',
                data: 'test',
                success: function (response) {
                    $('#progress-bar-level').progress({
                        percent: response['progress']
                    });
                }
            });
        }, 1000)
})
