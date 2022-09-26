function Sentence() {
    function bindEnvent() {
        $(".sentence_edit").click(function (e) {

            var params = {
                sentence: $(".sentence").val(),
                intent_id: $(".intent_id").val(),
                bot_id: $(".bot_id").val(),
                created_time: new Date()
            }

            console.log(params)
            var base_url = location.protocol + "//" + document.domain + location.port;

            $.ajax({
                url: base_url + "/sentence_detail/1",
                type : "PUT",
                data : params,
                data_type : "json",
                success: function (res) {
                    if (res) {
                        console.log("ress")
                        location.reload()
                    }
                }
            })

        })
    }
    bindEnvent()
}

$(document).ready(function () {
     Sentence()
})