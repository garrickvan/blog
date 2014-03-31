// init the uitoptop plugins.
$().UItoTop({ easingType: 'easeOutQuart' });

// 统计阅读次数
$('#read_counter').each(function() {
    $.post("/read_counter", { id : $(this).attr('target'), csrfmiddlewaretoken : $(this).attr('csrftoken') } );
})