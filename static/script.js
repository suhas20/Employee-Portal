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

//function for popovers
$(document).ready(function() {

  // Save notifications to local storage initially
  localStorage.setItem('notifications', JSON.stringify(notifications));
  console.log('Notifications saved to localStorage:', notifications);
  

  // Retrieve notifications from local storage
  var loadedNotifications = JSON.parse(localStorage.getItem('notifications')) || [];
  console.log('Loaded notifications array:', loadedNotifications);

  // Function to generate notification content with a close button
  function generateNotificationContent(notifications) {
    return notifications.map((notification, index) => 
      `${notification.Message} <span class="close-notification" data-index="${index}">&times;</span>`
    ).join('<br><hr class="custom-hr">');
  }

  // Function to update popover content and save to local storage
  function updatePopoverContent() {
    var content = notifications.length > 0 
      ? generateNotificationContent(notifications) 
      : 'No Notifications';

    console.log('Updated popover content:', content); // Debug log

    // Save notifications to local storage
    localStorage.setItem('notifications', JSON.stringify(notifications));
    
    // Destroy and reinitialize popover to force update
    var $popover = $('[data-toggle="popover"]');
    $popover.popover('dispose').popover({
      trigger: 'focus',
      content: content,
      html: true,
      placement: 'right'
    });

    // Manually show the popover to reflect the changes
    if ($popover.is(':focus')) {
      $popover.popover('show');
    }
  }

  // Initialize the popover
  var content = notifications.length > 0 
    ? generateNotificationContent(loadedNotifications) 
    : 'No Notifications';


  $('[data-toggle="popover"]').popover({
    trigger: 'focus',
    content: content,
    html: true,
    placement: 'right'
  });

  // Add click event to remove notification
  $(document).on('click', '.close-notification', function() {
    var index = $(this).attr('data-index');
    console.log('Removing notification at index:', index); // Debug log
    notifications.splice(index, 1); // Remove the notification from the array
    console.log('Updated notifications array:', notifications); // Debug log
    updatePopoverContent(); // Update the popover content
  });
});

  