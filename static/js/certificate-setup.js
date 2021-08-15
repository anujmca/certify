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
        async: false,
        url: url,
        dataType: 'JSON',
        type: isNew ? 'POST' : 'PATCH',
        data: payload,
        success:function(data){
            let id = $('#id').val();
            let wasNew = (!id || id == '' || id == undefined);
            if(wasNew) {
                $('#id').val(data.id);
                $('#event_id span').text(data.id);
                $('#event_id').removeAttr('hidden');
            }
        }
    });
}

function event_template_save()
{
    let selected_existing_template_id = $('input[name=existing-template]:checked').val(),
        event_id = $('#id').val();

    let template_id = -1;
    if (selected_existing_template_id != '' && selected_existing_template_id != undefined) {
        template_id = selected_existing_template_id;
    }

    payload={'template_id': template_id}
    let url = url_events + event_id + '/';

    $.ajax({
        async: false,
        url: url,
        dataType: 'JSON',
        type: 'PATCH',
        data: payload,
        success:function(data){
            return true;
        }
    });
}

function event_datasheet_save()
{
    let selected_existing_datasheet_id = $('input[name=existing-datasheet]:checked').val(),
        event_id = $('#id').val();

    let datasheet_id = -1;
    if (selected_existing_datasheet_id != '' && selected_existing_datasheet_id != undefined) {
        datasheet_id = selected_existing_datasheet_id;
    }

    payload={'datasheet_id': datasheet_id}
    let url = url_events + event_id + '/';

    $.ajax({
        async: false,
        url: url,
        dataType: 'JSON',
        type: 'PATCH',
        data: payload,
        success:function(data){
            return true;
        }
    });
}