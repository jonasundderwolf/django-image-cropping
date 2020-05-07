if (!String.prototype.endsWith) {
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/endsWith
    String.prototype.endsWith = function (searchString, position) {
        var subjectString = this.toString();
        if (typeof position !== 'number' || !isFinite(position) || Math.floor(position) !== position || position > subjectString.length) {
            position = subjectString.length;
        }
        position -= searchString.length;
        var lastIndex = subjectString.lastIndexOf(searchString, position);
        return lastIndex !== -1 && lastIndex === position;
    };
}

(function ($) {
    var className = 'image-ratio';

    if ((typeof jQ !== 'undefined') && (typeof jQ.fn.Jcrop === 'function')) {
        $ = jQ;
    }

    function createImage($item) {
        var $img, imageId;

        imageId = $item.attr('id') + '-image';
        $img = $('#' + imageId);
        if ($img.length > 0) {
            return $img;
        }

        $img = $('<img id="' + imageId + '" style="display: none; visibility: hidden;">');
        $img.insertAfter($item);

        return $img;
    }

    function loadedImage(img, fileUrl, $item, sourceWidth, sourceHeight) {
        var $img, imageId, imgScale, objUrl, options, ary, parentCls;

        parentCls = '.field-' + $item.data('my-name');
        $item.parents(parentCls + ':hidden:first').show();

        imageId = $item.attr('id') + '-image';
        $img = $('#' + imageId);
        if (img.type === 'error') {
            $img.removeAttr('src');

            $img = $item.parent().find('.jcrop-holder img');
            $img.removeAttr('src');
            return;
        }

        imgScale = loadImage.scale(img, {
            maxWidth: $item.data('box-max-width'),
            maxHeight: $item.data('box-max-height')
        });
        objUrl = loadImage.createObjectURL(fileUrl);
        $img.attr('src', objUrl);
        $img.css({
            'width': imgScale.width,
            'height': imgScale.height
        });

        if (typeof image_cropping.jcrop[imageId] === 'undefined') {
            options = {
                minSize: [5, 5],
                aspectRatio: $item.data('ratio'),
                boxWidth: $item.data('box-max-width'),
                boxHeight: $item.data('box-max-height'),
                trueSize: [sourceWidth, sourceHeight],
                onSelect: function (sel) {
                    $item.val([
                        Math.round(sel.x),
                        Math.round(sel.y),
                        Math.round(sel.x2),
                        Math.round(sel.y2)
                    ].join(','));
                }
            };

            if ($item.val() !== '') {
                // [ x,y,w,h ]
                ary = $item.val().split(',');
                if ((ary[0] + ary[2]) > sourceWidth) {
                    ary[0] = 0;
                }
                if ((ary[1] + ary[3]) > sourceHeight) {
                    ary[1] = 0;
                }
                options['setSelect'] = ary;
            } else {
                options['setSelect'] = [0, 0, sourceWidth / 2, sourceHeight / 2];
            }
            $img.Jcrop(options, function () {
                image_cropping.jcrop[imageId] = this;
            });
        } else {
            options = {
                boxWidth: $item.data('box-max-width'),
                boxHeight: $item.data('box-max-height'),
                trueSize: [sourceWidth, sourceHeight]
            };
            image_cropping.jcrop[imageId].setImage(objUrl);
            image_cropping.jcrop[imageId].setOptions(options);

            if ($item.val() !== '') {
                // [ x,y,w,h ]
                ary = $item.val().split(',');
                if ((ary[0] + ary[2]) > sourceWidth) {
                    ary[0] = 0;
                }
                if ((ary[1] + ary[3]) > sourceHeight) {
                    ary[1] = 0;
                }
            } else {
                ary = [0, 0, sourceWidth / 2, sourceHeight / 2];
            }
            image_cropping.jcrop[imageId].setSelect(ary);
        }
    }

    function findTarget(target) {
        var $target = target, ary = [];

        if ($.isArray(target)) {
            $(target).each(function (idx, item) {
                var $item = $(item);

                if (!$item.hasClass(className)) {
                    $item.find('.' + className).each(function (i, node) {
                        ary.push(node);
                    });
                } else {
                    ary.push(item);
                }
            });
            $target = $(ary);
        } else {
            if (typeof target === 'string') {
                $target = $(target);
            }

            if (!$target.hasClass(className)) {
                $target = $target.find('.' + className);
            }
        }

        return $target;
    }

    var count = 0, maxCount = 200;
    function init() {
        var line = {}, key;

        if (typeof loadImage !== 'function') {
            if (count > maxCount) {
                return;
            }

            count += 1;
            setTimeout(init, 500);
            return;
        }

        count = 0;
        $('.image-ratio').each(function (idx, node) {
            var $node = $(node), imgField, name, prefix, $inlineGroup;

            $inlineGroup = $node.parents('.inline-group:first');
            if (($inlineGroup.length > 0) && ($inlineGroup.data('bind-load-image') !== 'binded')) {
                $inlineGroup.find('.add-row').click(function () {
                    window.bindLoadImage();
                });
                $inlineGroup.data('bind-load-image', 'binded');
            }

            name = $node.attr('name');
            prefix = name.replace($node.data('my-name'), '');
            if (prefix.endsWith('__prefix__-')) {
                return;
            }

            imgField = prefix + $node.data('image-field');
            if (!line.hasOwnProperty(imgField)) {
                line[imgField] = [];
            }
            line[imgField].push(node);
        });

        for (key in line) {
            if (line.hasOwnProperty(key)) {
                findTarget(line[key]).each(function (idx, item) {
                    // 產生 image tag
                    createImage($(item));
                });

                $('input[name="' + key + '"]').each(function (idx, node) {
                    var $target = findTarget(line[key]), $node = $(node);

                    if (($target.length <= 0) || (typeof loadImage !== 'function')) {
                        return false;
                    }

                    if ($node.data('bind-load-image') === 'binded') {
                        return;
                    }

                    $node
                        .on('change', function (e) {
                            var w, h;
                            // 載入圖片
                            loadImage(
                                e.target.files[0],
                                function (img) {
                                    w = img.width;
                                    h = img.height;
                                    $target.each(function (i, item) {
                                        loadedImage(img, e.target.files[0], $(item), w, h);
                                    });
                                },
                                {} // Options
                            );
                        })
                        .data('bind-load-image', 'binded');
                });
            }
        }
    }
    $(function () {
        window.bindLoadImage = function () {
            init();
        }
        init();
    });
}(jQuery));
