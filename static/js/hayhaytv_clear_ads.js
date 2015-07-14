console.log('Clear hayhayads loaded');
for (element in window) {
    if (element.indexOf('adsXMLURL') == 0) {
        console.log(element);
        window[element] = "";
    }
}
autostartFilm = true;
$(".banner_player_img").hide();
addPlayer(initVideoUrl, imageSrc, null, null, videoSubs);
$(".info_film-div").hide();
setTimeout(function () {
    $('body').html($('#new_player_wrapper').html());
    $('body').css({width: '100%', height: '100%', position: 'absolute'});
    $('object').css('position', 'relative');
}, 500);