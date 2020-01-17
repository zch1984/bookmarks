(function(){
    var jquery_version = '3.3.1';
    var site_url = 'https://e0d2ccfc.ngrok.io/';
    var static_url = site_url + 'static/';
    var min_width = 100;
    var min_height = 100;

    function bookmarklet(msg){
        // load CSS
        var css = jQuery('<link>');
        css.attr({
            rel: 'stylesheet',
            type: 'text/css',
            // 使用随机数作为参数加载bookmarklet.css样式表，防止浏览器返回一个缓存文件
            href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999999)
        });
        jQuery('head').append(css);  // 将当前站点的head标签添加css样式

        // load HTML
        // 定义一个html样式
        box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>>';
        jQuery('body').append(box_html);  // 将该样式添加到当前站点的<body>文档元素中

        // close event
        // 通过jQuery提取id为bookmarklet的父元素和id为close的下属元素，通过#ID的方式获取
        jQuery('#bookmarklet #close').click(function(){
            jQuery('#bookmarklet').remove();
        });

        // find images and display them
        // src$="jpg" 选择去获取所有<img>HTML元素，其src属性以jpg字符串结尾。
        jQuery.each(jQuery('img[src$="jpg"]'), function(index, image){
            // 如果图片的大小超过规定值，则将其放置到<div class="images">HTML容器中。
            if(jQuery(image).width() >= min_width && jQuery(image).height() >= min_height){
                image_url = jQuery(image).attr('src');
                jQuery('#bookmarklet .images').append('<a href="#"><img src="' + image_url + '" /></a>>');
            }
        });

        // when an image is selected open URL with it
        jQuery('#bookmarklet .images a').click(function(e){
            selected_image = jQuery(this).children('img').attr('src');
            // hide bookmarklet
            jQuery('#bookmarklet').hide();
            // open new window to submit the image
            window.open(site_url + 'images/create/?url=' + encodeURIComponent(selected_image) + '&title=' + encodeURIComponent(jQuery('title').text()) + '_blank');
        });

    };

    // Check if jQuery is loaded
    if(typeof window.jQuery != 'undefined'){
        bookmarklet();
    } else {
        // Check for conflicts
        var conflict = typeof window.$ != 'undefined';
        // Create the script and point to Google API
        var script = document.createElement('script');
        // https://code.jquery.com/jquery-3.4.1.min.js
        script.src = '//code.jquery.com/jquery-' + jquery_version + '/jquery.min.js';
        // Add the script to the 'head' for processing
        document.head.appendChild(script);
        // Create a way to wait until script loading
        var attempts = 15;
        (function () {
            // Check again if jQuery is undefined
            if(typeof window.jQuery == 'undefined'){
                if(--attempts > 0){
                    // Calls himself in a few milliseconds
                    window.setTimeout(arguments.callee, 250)
                } else {
                    // Too much attempts to load,send error
                    alert('An error ocurred while loading jQuery')
                }
            } else {
                bookmarklet();
            }
        })();
    }
})()