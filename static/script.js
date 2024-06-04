$(document).ready(function() {
    $('.clickable-row').click(function() {
        var taskId = $(this).data('task-id');
        console.log('Fetching details for task ID:', taskId);
        $.ajax({
            url: '/task/' + taskId,
            method: 'GET',
            success: function(data) {
                console.log('Data fetched:', data);
                if (data.error) {
                    alert(data.error);
                } else {
                    $('#TaskID').text(data.TaskID);
                    $('#EmpName').text(data.EmpName);
                    $('#CreatedOn').text(data.CreatedOn);
                    $('#ShortDescription').text(data.ShortDescription);
                    $('#WorkNotes').text(data.WorkNotes);
                    $('#taskModal').modal('show');
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error fetching task details:', textStatus, errorThrown);
            }
        });
    });
});

//funtion to select hours
$(document).ready(function () {
    const hours = $('#Hours');
    const min = $('#Min');
    for (let i = 1; i <= 12; i++) {
        hours.append(new Option(i, i));
    }
    for(let i = 10; i <= 60; i+=10){
        min.append(new Option(i,i));
    }
});
