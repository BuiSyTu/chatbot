$(document).ready(function() {
    $(document).off('click', '[btn-delete');
    $(document).on('click', '[btn-delete]', function () {
       const id = $(this).attr('data-id');
       alert(id);
    });

    $(document).off('click', '[btn-edit');
    $(document).on('click', '[btn-edit]', function () {
        $("#edit-user").modal('toggle');
        const id = $(this).attr('data-id');
        $.ajax({
            url: `/api/users/${id}`,
            method: 'GET',
            success: function (res){
                $('#edit-user').find('[name=username]').val(res.username);
                $('#edit-user').find('[name=password]').val(res.password);
            }
        });

        $('#edit-user').off('click', '[btn-cancel]');
        $('#edit-user').on('click', '[btn-cancel]', function() {
            const username = $('#edit-user').find('[name=username]').val();
            const password = $('#edit-user').find('[name=password]').val();
        })

        $('#edit-user').on('click', '[btn-save]', function() {

        })
    });
});