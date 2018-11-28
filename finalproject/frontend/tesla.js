var wordData = [];
$(document).ready(function () {
    $.ajax({
        url: "stockQuery.php",
        timeout: 10000,
        dataType: "json",
        success: function (data) {
            console.log(data);
        }
    });
        $.ajax({
            url: "wordCountQuery.php",
            dataType: "json",
            success: function (data) {
               // console.log(data);
                console.log(data);
            },
            error: function (e) {
                console.log(e);
            }
        });
});/**
 * Created by Matt on 11/24/2018.
 */

function print() {
    if(wordData.length === 73){
        console.log(wordData);

    }
}
function sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; i < 1e7; i++) {
        if ((new Date().getTime() - start) > milliseconds){
            break;
        }
    }
}
