var count_images = 1
var count = 1
var count_used = 0
var max_count = 15


function addImage(num) {
    if (count_used >= max_count)
        return ""
    let block = document.createElement('div');
    block.className = "input-file-row-1";
    block.innerHTML = '<div class="upload-file-container"><div class="delete-image hidden"></div><img id="image'+count_images+'" class="this-is-image" src="#" alt=""/><input type="file" name="image'+count_images+'" class="photo" id="imgInput'+count_images+'"/></div>';
    document.getElementById("images"+num).append(block);
    count_images += 1;
    count += 1;
}

function readURL(input) {
    if (input.files && input.files[0]) {
        var num = parseInt(input.id.match(/\d+/))
        var fr = new FileReader();
        fr.onload = function () {
            if (input.files[0].name.endsWith(".mp4")) {
                $('#image'+num).attr('src', '/static/img/video.png');
            } else {
                $('#image'+num).attr('src', fr.result);
            }
            if ($('#image'+num).attr('class') === 'this-is-image' || $('#image'+num).attr('class') === '') {
                count_used += 1;
                addImage(parseInt($($($(input).closest('.settings-images')).children()[0]).attr('id').match(/\d+/)));
                $('#image'+num).toggleClass("visible");
                $($($('#image'+num).closest('.upload-file-container')[0]).children()[0]).toggleClass("hidden");
            }
        }
        fr.readAsDataURL(input.files[0]);
    }
}


$("body").delegate('[id^="imgInput"]', "change", function(){
    readURL(this)
});

$('[id^="image"]').each(function(){
    count_images += 1;
    count += 1;
    if ($(this).attr('src') !== "" && $(this).attr('src') !== "#" && $(this).attr('src') !== undefined) {
        count_used += 1;
    }
});


$("body").delegate('[id^="addImage"]', "click", function() {
    var num = parseInt(this.id.match(/\d+/))
    addImage(num);
});

$("body").delegate('.delete-image', "click", function(){
    var num = parseInt($($(this).closest('[id^="images"]')[0]).attr('id').match(/\d+/))
    count -= 1;
    var father = $(this).closest('.input-file-row-1');
    var src = $($(father.children()[0]).children()[1]).attr('src');
    if (!(src === undefined || src === '' || src === '#')) {
        count_used -= 1;
        $(this).closest('.input-file-row-1').remove();
        if (count_used + 1 == max_count) {
            addImage(num);
        }
    }
});