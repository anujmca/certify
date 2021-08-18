let url_generate = '/services/certificates/generate';

function generate_certificate(event_id)
{
    let csrf_token = $('[name="csrfmiddlewaretoken"]').val();

    payload={'event_id': event_id}

    $.ajax({
        async: false,
        url: url_generate,
        headers:{"X-CSRFToken": csrf_token},
        dataType: 'JSON',
        type: 'POST',
        data: payload,
        success:function(data){
            if(data.result == 'success'){
                $('#exampleModalCenter').modal("show");
                $('#status_' + data.id).text("Generated");
                $('#action_' + data.id).html('<a href="/certificates/generated" class="btn btn-primary">Details</a><a href="javascript:generate_certificate(' + data.id + ')">Regenerate</a>');
            }
        }
    });
}