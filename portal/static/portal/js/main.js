/*
 * main.js
 * pc @ 20170620
 */

/*
 * 用途：生成顶部菜单的数据
 * json_file： 提供 json 数据来源
 */
function loadNavTop(json_file){
    $("ul#navbar_top").empty();
    $.getJSON(json_file,function(result){
        var content = '';
        $.each(result.data, function(idx_i, item_i){
            $.each(item_i.nodes, function(idx_j, item_j){

                content = ''
                        + '<!-- navbar_top Start-->'
                        + '<li class="dropdown">'
                            + '<a href="#" class="dropdown-toggle" data-toggle="dropdown">' + item_j.text + '<b class="caret"></b></a>'
                            + '<ul class="dropdown-menu">';

                $.each(item_j.nodes, function(idx_k, item_k){
                    content += ''
                                + '<li><a id="appid" href="' + item_k.href + '">' + item_k.text + '</a></li>';
                });

                content += ''
                            + '</ul>'
                        + '</li>';

                 $("ul#navbar_top").append(content);
            });
        });
    });
}


/*
 * 用途：生成左侧侧边栏的数据
 * json_file： 提供 json 数据来源
 */
function loadContentLeftTreeView(json_file) {
    $.getJSON(json_file,function(result){
        $('div#tree').treeview({
            data: result.data,
            levels: 3,
            showBorder: false,
            expandIcon: 'glyphicon glyphicon-chevron-right',
            collapseIcon: 'glyphicon glyphicon-chevron-down',
            nodeIcon: 'glyphicon glyphicon-link',
            enableLinks: true
        });
    });
}


/*
 * 用途：生成右侧内容栏的数据
 * json_file： 提供 json 数据来源
 */
function loadContentRight(json_file){
    $("div#panel_lists").empty();
    $("h2#sub_header").empty();
    $.getJSON(json_file,function(result){
        //console.info(result.data);
        $("h2#sub_header").append(result.title);
        $.each(result.data, function(idx_i, item_i){
            var content = '';

            content = ''
                + '<!-- panel Start-->'
                + '<div class="panel" id="links_online">'
                    + '<div class="panel-heading">'
                        + '<span class="panel-title">'
                            + '<a class="accordion-toggle" data-toggle="collapse" data-parent="#links_online" href="#collapse_' + idx_i + '">'
                                + '<strong id="this_title" class="label label-success label-tag">' + item_i.name + '</strong>'
                            + '</a>'
                        + '</span>'
                    + '</div>'
                + '';

            content += ''
                    + '<div id="collapse_' + idx_i + '" class="panel-collapse in">'
                        + '<div class="panel-body placeholders">'
                + '';

            $.each(item_i.links, function(idx_j, item_j){
                content += ''
                            + '<div class="col-xs-4 col-sm-2 placeholder">'

                                + '<a class="portal" target="_blank" href="' + item_j.href + '">'
                                    + '<img src="' + item_j.img + '" class="img-item-list img-responsive">'
                                    + '<h5 class="text-muted">' + item_j.name + '</h5>'
                                + '</a>'
                            + '</div>'
                + '';
            });

            content += ''
                        + '</div>'
                    + '</div>'
                + '</div>'
                + '<!-- End of panel-->'
                + '';

             $("div#panel_lists").append(content);
        });
    });

}


/*
 * 用途：页面加载后的操作
 */
$(document).ready(function(){
    //页面首次加载

    //加载顶部菜单
    loadNavTop('/portal/show/tree');

    //加载左侧的侧边栏 treeview
    loadContentLeftTreeView('/portal/show/tree');

    //默认内容
    var curr_uri = $(this).context.URL;
    //console.info('find #appid_ from URL position: ' + curr_uri.search('#appid_'))
    if (curr_uri.search('#appid_') == -1) {
        loadContentRight('/portal/show/app/default');
    }
    else {
        var curr_app_id = curr_uri.split("#")[1].slice(6);
        loadContentRight('/portal/show/app/' + curr_app_id);
    }

    // treeview 的节点选中事件响应【js动态生成的选择器】
    $(document).on('nodeSelected', 'div#tree', function(event, data) {
        if (data.href && data.href.length > 1) {
            var json_file_tree_node = '/portal/show/app/' + data.href.slice(7);
            loadContentRight(json_file_tree_node);
        }
    });

    //<a href="#appid_xxx"> 的单击事件响应【js动态生成的选择器】
    $(document).on('click', 'a#appid', function() {
        var json_file_nav = '/portal/show/app/' + $(this).context.hash.slice(7);
        loadContentRight(json_file_nav);
    });

});
