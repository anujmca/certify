let url_generate = '/services/certificates/1/sms/send';

function send_sms(certificate_id)
{
    let csrf_token = $('[name="csrfmiddlewaretoken"]').val();

    payload={'certificate_id': certificate_id}

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

function send_email(certificate_id)
{
    let csrf_token = $('[name="csrfmiddlewaretoken"]').val();

    payload={'certificate_id': certificate_id}

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

function public_certificate_copy_to_clipboard(certificate_id){
    let public_url = window.location.protocol + "//" + window.location.host + '/public/certificates/' + certificate_id + '/view';
    copyToClipboard(public_url);

    alert('Copied to your clipboard');
}