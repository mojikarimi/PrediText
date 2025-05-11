// For Image
function readURL(input) {
    if (input.files && input.files[0]) {

        var reader = new FileReader();

        reader.onload = function(e) {
            $('.image-upload-wrap').hide();

            $('.file-upload-image').attr('src', e.target.result);
            $('.file-upload-content').show();
        };

        reader.readAsDataURL(input.files[0]);

    } else {
        removeUpload();
    }
}
function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
    $('.file-upload-input').remove()
    $('.image-upload-wrap').prepend('<input class="file-upload-input" type=\'file\' onchange="readURLvideo(this);"\n' +
        '                                           accept="image/*"/>')
}
$('.image-upload-wrap').bind('dragover', function () {
    $('.image-upload-wrap').addClass('image-dropping');
});
$('.image-upload-wrap').bind('dragleave', function () {
    $('.image-upload-wrap').removeClass('image-dropping');
});


// For Video
function readURLvideo(input) {
    if (input.files && input.files[0]) {

        var reader = new FileReader();

        reader.onload = function(e) {
            $('.image-upload-wrap').hide();
            $('.file-upload-video').attr('src', URL.createObjectURL(input.files[0]));
            $('.file-upload-content').show();

        };
        reader.readAsDataURL(input.files[0]);

    } else {
        removeUploadvideo();
    }
}

function removeUploadvideo() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
    $('.file-upload-video').attr('src', '#');
    $('.file-upload-input').remove()
    $('.image-upload-wrap').prepend('<input class="file-upload-input" type=\'file\' onchange="readURLvideo(this);"\n' +
        '                                           accept="video/mp4"/>')
}

$('.image-upload-wrap').bind('dragover', function () {
    $('.image-upload-wrap').addClass('image-dropping');
});
$('.image-upload-wrap').bind('dragleave', function () {
    $('.image-upload-wrap').removeClass('image-dropping');
});