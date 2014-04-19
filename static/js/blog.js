// init the uitoptop plugins.
$().UItoTop({ easingType: 'easeOutQuart' });

// 统计阅读次数
$('#read_counter').each(function() {
    $.post("/read_counter", { id : $(this).attr('target'), csrfmiddlewaretoken : $(this).attr('csrftoken') } );
})

// 搜索框
$('#searching_by_engine_btn').click(function() {
    window.location.href = '/search?q=' + $('#searching_by_engine_input').val()
})