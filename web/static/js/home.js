// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api_v1/users',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(fname, lname, age, job) {
            let ajax_options = {
                type: 'POST',
                url: 'api_v1/users',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'fname': fname,
                    'lname': lname,
                    'age': age,
                    'job': job

                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(fname, lname, age, job) {
            let ajax_options = {
                type: 'PUT',
                url: 'api_v1/users/' + lname,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'fname': fname,
                    'lname': lname,
                    'age': age,
                    'job': job
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'delete': function(lname) {
            let ajax_options = {
                type: 'DELETE',
                url: 'api_v1/users/' + lname,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $fname = $('#fname'),
        $lname = $('#lname'),
        $age = $('#age'),
        $job = $('#job');

    // return the API
    return {
        reset: function() {
            $lname.val('');
            $fname.val('').focus();
            $age.val('');
            $job.val('');
        },
        update_editor: function(fname, lname, age, job) {
            $lname.val(lname);
            $fname.val(fname).focus();
            $age.val('');
            $job.val('');
        },
        build_table: function(users) {
            let rows = '';

            // clear the table
            $('.users table > tbody').empty();

            // did we get a users array?
            if (users) {
                for (let i=0, l=users.length; i < l; i++) {
                    rows += `<tr><td class="fname">${users[i].fname}</td><td class="lname">${users[i].lname}</td><td>${users[i].timestamp}</td><td>${users[i].age}</td><td>${users[i].job}</td></tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $fname = $('#fname'),
        $lname = $('#lname'),
        $age = $('#age'),
        $job = $('#job');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(fname, lname, age, job) {
        return fname !== "" && lname !== "" && age !== 0 && job !== "";
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let fname = $fname.val(),
            lname = $lname.val(),
            age = $age.val(),
            job = $job.val();

        e.preventDefault();

        if (validate(fname, lname, age, job)) {
            model.create(fname, lname, age, job)
        } else {
            alert('Problem with first or last name input');
        }
    });

    $('#update').click(function(e) {
        let fname = $fname.val(),
            lname = $lname.val(),
            age = $age.val(),
            job = $job.val();

        e.preventDefault();

        if (validate(fname, lname, age, job)) {
            model.update(fname, lname, age, job)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let lname = $lname.val();

        e.preventDefault();

        if (validate('placeholder', lname)) {
            model.delete(lname)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    });

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            fname,
            lname,
            age,
            job;

        fname = $target
            .parent()
            .find('td.fname')
            .text();

        lname = $target
            .parent()
            .find('td.lname')
            .text();
        age = $target
            .parent()
            .find('td.age')
            .text();
        job = $target
            .parent()
            .find('td.job')
            .text();

        view.update_editor(fname, lname, age, job);
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));
