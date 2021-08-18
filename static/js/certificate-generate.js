let url_generate = '/services/certificates/generate';

function generate_certificate(event_id)
{
    let csrf_token = $('[name="csrfmiddlewaretoken"]').val();

    payload={'event_id': event_id}

    $.ajax({
        async: true,
        url: url_generate,
        headers:{"X-CSRFToken": csrf_token},
        dataType: 'JSON',
        type: 'POST',
        data: payload,
        success:function(data){
            console.log(data);
            alert(data);
        }
    });
}