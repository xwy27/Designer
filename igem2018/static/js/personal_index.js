let $msg_modal = $('#msg-modal');
let $msg_body = $('#msg-body');
let $msg_head = $('#msg-header')
function get_circuits(name, authority) {
    $.get('/api/authority_circuits', {
        name: JSON.stringify(name)
    }, function (res) {
        if (res.circuits.length > 0) {
            $('#circuits-modal div h5').html(`Circuit Name: ${name}`);
            let html =
                `<thead>
                <tr>
                    <th class="sorted descending">ID</th>\
                    <th class="sorted descending">Editor</th>\
                    <th class="sorted descending">Update Time</th>\
                    <th class="sorted descending">Comment</th>\
                `
            html += `</tr></thead><tbody>`

            $('#circuits-table').append(html);
            res.circuits.forEach(element => {
                let temp = `<tr data-id="${element.ID}">\
                    <td class="id">${element.ID}</td>\
                    <td>${element.Editor}</td>\
                    <td>${element.UpdateTime}</td>\
                    <td>${element.Comment}</td>`;
                $('#circuits-table').append(temp + `</tr></tbody>`);
            });
            $('#circuits-table').children('tbody').children('tr').on('click', function () {
                let id = $(this).attr('data-id');
                let url = `/design/${id}`;
                if (authority === 'share-table') {
                    url = `/design/share/${id}`;
                }
                window.location = url;
            });
            $('table').tablesort();
        } else {
            $('#circuits-table').html('<h5 class="ui center aligned">Empty!</h5>');
        }
    });
}

let id;
function refresh() {
    $.get('/api/authority?circuit=' + id, function (res) {
        if (res.read.length > 0) {
            $('#view-users').html(`<div class="ui list">`);
            res.read.forEach(function (ele) {
                $('#view-users').append(
                    `<div class="item">
                        <div class="content">
                            <i class="users icon"></i>${ele}<i class="red delete icon authority-delete"></i>
                        </div>
                        <div class="ui divider"></div>
                    </div>`);
            });
            $('#view-users').append(`</div>`);
        } else {
            $('#view-users').html('<h5 class="ui center aligned">Share your design to others!</h5>');
        }
        if (res.write.length > 0) {
            $('#edit-users').html(`<div class="ui list">`);
            res.write.forEach(function (ele) {
                $('#edit-users').append(
                    `<div class="item">
                        <div class="content">
                            <i class="users icon"></i>${ele}<i class="red delete icon authority-delete"></i>
                        </div>
                        <div class="ui divider"></div>
                    </div>`);
            });
            $('#edit-users').append(`</div>`);
        } else {
            $('#edit-users').html('<h5 class="ui center aligned">Share your design to others!</h5>');
        }

        $('.authority-delete').on('click', function () {
            var username = $(this).parent()[0].innerText;
            $msg_body.text('Your alteration is sending to the server.');
            $msg_modal.modal('show');
            $.ajax({
                type: 'DELETE',
                url: '/api/authority_delete',
                data: {
                    'username': username,
                    'design': id,
                },
                success: (res) => {
                    setTimeout(() => {
                        $msg_body.text('Success.')
                        setTimeout(() => {
                            $msg_modal.modal('hide');
                        }, 2000);
                    }, 500);
                    // res.status == 0 -> error
                    // res.status == 1 -> success
                    refresh(id);
                }
            })
        });
    });
}

$('#search-users-dropdown').dropdown({
    apiSettings: {
        url: '/api/users?username={query}',
        cache: false,
        beforeSend: (settings) => {
            return settings.urlData.query.length < 1 ? false : settings;
        },
        onResponse: (response) => ({
            success: response.success === true,
            results: response.users.map((x) => ({
                name: x.username,
                value: x.username
            }))
        })
    }
}).popup({
    content: 'Search a user (Case Sensitive)'
});

$('#msg-modal').modal({
    allowMultiple: true
});
$('#share-view-button, #share-edit-button').on('click', function (event) {
    if ($('#search-users-dropdown').dropdown('get value').length > 0) {
        $msg_body.text('Your alteration is sending to the server.');
        $msg_modal.modal('show');
        let data = {
            users: JSON.stringify($('#search-users-dropdown').dropdown('get value')),
            circuit: JSON.stringify(id),
            authority: JSON.stringify(
                event.target.innerText === 'Share view' ? 'read' : 'write'
            )
        };
        $.post('/api/authority', data, function (v) {
            setTimeout(() => {
                $msg_body.text('Success');
                setTimeout(() => {
                    $msg_modal.modal('hide');
                }, 2000);
            }, 500);
            refresh();
        });
    }
});

$(function () {
    $('#master-table, #share-table').children('tbody').children('tr').on('click', function () {
        let name = $(this).attr('data-name')
        get_circuits(name, $(this).parent().first().parent().first().attr('id'));
        $('#circuits-modal').modal({
            onHide: function () {
                $('#circuits-table').html('');
            }
        }).modal('show');
    });
    $('#part-table').children('tbody').children('tr')
        .on('click', function () {
            let data = {
                "part" : {
                    "type" : "unknown",
                    "name" : "unknown",
                    "id" : $(this).attr('data-id'),
                    "description" : "unknown"
                }
            };
            //console.log(data);
            let itemModal = $('#inspect-item-modal');
            itemModal.modal('show');
            // TODO: type and role is (incorrectly) the same here.
            // change it when "type and role" is fixed.
            $.ajax('/api/part', {
                data: {
                    id: data['part']['id']
                },
                success: (data) => {
                    itemModal
                        .find('input[name=component-role]')
                        .val(data['type']);
                    itemModal
                        .find('input[name=component-id]')
                        .val(data['name']);
                    itemModal
                        .find('input[name=component-name]')
                        .val(data['name']);
                    itemModal
                        .find('textarea[name=component-description]')
                        .val(data['description']);
                    itemModal
                        .find('textarea[name=component-sequence]')
                        .val(data['sequence']);
                }
            });
        });
    $('#authority-table').children('tbody').children('tr').on('click', function () {
        id = $(this).attr('data-id');
        refresh();
        $('#share-tab .item').tab();
        $('#share-modal').modal({
            onHide: function () {
                $('#search-users-dropdown').dropdown('clear');
            }
        }).modal('show');
    });
});

$('#logout').on('click', function () {
    window.location.href = '/logout';
});

$('.tabular.menu .item').tab();

$('table').tablesort();