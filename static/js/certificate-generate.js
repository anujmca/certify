const url_generate = '/services/certificates/generate';
const url_publish = '/services/certificates/publish';
const url_publish_individual = '/services/certificates/{certificate_id}/publish';

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


function publish_certificates(event_id)
{
    // alert('will publish');
    let csrf_token = $('[name="csrfmiddlewaretoken"]').val();

    payload={'event_id': event_id}

    $.ajax({
        async: false,
        url: url_publish,
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

function publish_certificate(certificate_id)
{
    // alert('will publish');
    let csrf_token = $('[name="csrfmiddlewaretoken"]').val();

    // payload={'event_id': event_id}

    $.ajax({
        async: false,
        url: url_publish_individual.replace('{certificate_id}', certificate_id),
        headers:{"X-CSRFToken": csrf_token},
        dataType: 'JSON',
        type: 'POST',
        data: null,
        success:function(data){
            if(data.result == 'success'){
                $('#exampleModalCenter').modal("show");
                $('#status_' + data.id).text("Generated");
                $('#action_' + data.id).html('<a href="/certificates/generated" class="btn btn-primary">Details</a><a href="javascript:generate_certificate(' + data.id + ')">Regenerate</a>');
            }
        }
    });
}