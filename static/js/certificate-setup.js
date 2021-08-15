let url_events = '/services/events/';

function event_information_save()
{
    let id = $('#id').val(),
        name = $('#name').val(),
        awarded_by = $('#awarded_by').val();

    let isNew = (!id || id == '' || id == undefined),
        payload={'name': name, 'awarded_by': awarded_by}

    let url = url_events + (isNew ? '' : id + '/');

    $.ajax({
        url: url,
        dataType: 'JSON',
        type: isNew ? 'POST' : 'PATCH',
        data: payload,
        success:function(data){
            let id = $('#id').val();
            let isNew = (!id || id == '' || id == undefined);
            if(isNew)
                $('#id').val(data.id);
        }
    });
}