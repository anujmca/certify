let url_events = '/services/events/',
    url_templates = '/services/templates/',
    url_datasheets = '/services/datasheets/';;

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

function template_save(){
    let id = ($('#template_id').length ? $('#template_id').val() : ''),
        name = $('#template_name').val(),
        description = $('#template_description').val();

    let isNew = (!id || id == '' || id == undefined);

    let payload = new FormData();
    let files = $('#event_template_file')[0].files;

    // Check file selected or not
    if(files.length > 0 )
       payload.append('file',files[0]);

    payload.append('name', name);
    payload.append('description', description);

    let url = url_templates + (isNew ? '' : id + '/');

    $.ajax({
        async: false,
        url: url,
        // dataType: 'JSON',
        cache: false,
        contentType: false,
        processData: false,
        type: isNew ? 'POST' : 'PATCH',
        data: payload,
        success:function(data){
            id = data.id;
            let template_id = ($('#template_id').length ? $('#template_id').val() : '');
            let wasNew = (!template_id || template_id == '' || template_id == undefined);
            if(wasNew && $('#template_id').length) {
                $('#template_id').val(data.id);
            }
        }
    });

    return id;
}

function datasheet_save(){
    let id = ($('#datasheet_id').length ? $('#datasheet_id').val() : ''),
        name = $('#datasheet_name').val(),
        description = $('#datasheet_description').val();

    let isNew = (!id || id == '' || id == undefined);

    let payload = new FormData();
    let files = $('#event_datasheet_file')[0].files;

    // Check file selected or not
    if(files.length > 0 )
       payload.append('data_sheet',files[0]);

    payload.append('name', name);
    payload.append('description', description);

    let url = url_datasheets + (isNew ? '' : id + '/');

    $.ajax({
        async: false,
        url: url,
        // dataType: 'JSON',
        cache: false,
        contentType: false,
        processData: false,
        type: isNew ? 'POST' : 'PATCH',
        data: payload,
        success:function(data){
            id = data.id;
            let datasheet_id = ($('#datasheet_id').length ? $('#datasheet_id').val() : '');
            let wasNew = (!datasheet_id || datasheet_id == '' || datasheet_id == undefined);
            if(wasNew && $('#datasheet_id').length) {
                $('#datasheet_id').val(data.id);
            }
        }
    });

    return id;
}

function event_template_save()
{
    let selected_existing_template_id = $('input[name=existing-template]:checked').val(),
        event_id = $('#id').val();

    let template_id = -1;
    if (selected_existing_template_id != '' && selected_existing_template_id != undefined) {
        template_id = selected_existing_template_id;
    }
    else{
        template_id = template_save();
    }

    let payload={'template_id': template_id}
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
    else{
        datasheet_id = datasheet_save();
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