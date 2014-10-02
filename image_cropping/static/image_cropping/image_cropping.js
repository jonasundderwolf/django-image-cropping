var image_cropping = function ($) {

    function init() {
      $('input.image-ratio').each(function() {
        var $this = $(this);

        var url = $(location).attr('href');
        url = url.replace($(location).attr('hash'), '');
        url = url.replace($(location).attr('search'), '');
        url = url + 'cropping_thumbnail/' + $this.data('image-field') + '/';

        // hide textfield
        $this.hide();
        // add status indicator
        var $indicator = $('<div><div></div></div>').addClass('cropping-status');
        $this.after($indicator);

        $indicator.addClass('loading');
        // load thumbnail
        $.getJSON(url)
          .fail(function() {
            $indicator.addClass('error');
          }).done(function($data) {
            var image_id = $this.attr('id') + '-image',
                org_width = $data['org-width'],
                org_height = $data['org-height'],
                min_width = $this.data('min-width'),
                min_height = $this.data('min-height');

            var is_image_portrait = (org_height > org_width);
            var is_select_portrait = (min_height > min_width);

            if ($this.data('adapt-rotation') === true) {
              if (is_image_portrait != is_select_portrait) {
                // cropping height/width need to be switched, picture is in portrait mode
                var x = min_width;
                min_width = min_height;
                min_height = x;
              }
            }

            var $image = $('<img>', {
              'id': image_id,
              'src': $data['thumb-url']
            }).insertAfter($this);
            $image.load(function() {
                $indicator.hide();
            });

            var options = {
              minSize: [5, 5],
              keySupport: false,
              trueSize: [org_width, org_height],
              onSelect: update_selection($this),
              addClass: ($this.data('size-warning') && ((org_width < min_width) || (org_height < min_height))) ? 'size-warning jcrop-image': 'jcrop-image',
              setSelect:initial_cropping($this.val()) // load initial cropping
            };
            if ($this.data('ratio')) {
              options['aspectRatio'] = $this.data('ratio');
            }

            var jcrop = {};
            $('#' + image_id).Jcrop(options, function(){jcrop[image_id]=this;});

            var cropping_disabled = false;
            if ($this.val()[0] == "-"){
              cropping_disabled = true;
              $this.val($this.val().substr(1));
            }

            if ($this.data('allow-fullsize') === true) {
              if(cropping_disabled){
                jcrop[image_id].release();
                $this.val('-'+$this.val());
              }
              var label = 'allow-fullsize-'+image_id;
              var checked = cropping_disabled ? '' : ' checked="checked"';
              var fullsize = $('<div class="field-box allow-fullsize">' +
                               '<input type="checkbox" id="'+label+'" name="'+label+'"'+checked+'></div>');

              if ($this.parent().find('.help').length) {
                fullsize.insertBefore($this.parent().find('.help'));
              } else {
                fullsize.appendTo($this.parent());
              }

              $('#'+label).click(function(){
                if (cropping_disabled === true){
                  $this.val($this.val().substr(1));
                  jcrop[image_id].setSelect($this.val().split(','));
                  cropping_disabled = false;
                } else {
                  $this.val('-'+$this.val());
                  jcrop[image_id].release();
                  cropping_disabled = true;
                }
              });
              $this.parent().find('.jcrop-tracker').mousedown(function(){
                  if (cropping_disabled){
                    $('#'+label).attr('checked','checked');
                    cropping_disabled = false;
                  }
              });
            }
          });
      });
    }

    function initial_cropping (val) {
      if (val === '') { return; }
      var s = val.split(',');
      return [
        parseInt(s[0], 10),
        parseInt(s[1], 10),
        parseInt(s[2], 10),
        parseInt(s[3], 10)
      ];
    }

    function _update_selection (sel, $crop_field) {
      if ($crop_field.data('size-warning')) {
        crop_indication(sel, $crop_field);
      }
      $crop_field.val(new Array(
        Math.round(sel.x),
        Math.round(sel.y),
        Math.round(sel.x2),
        Math.round(sel.y2)
      ).join(','));
    }

    function update_selection ($crop_field) {
      return function(sel) { _update_selection(sel, $crop_field); };
    }

    function crop_indication (sel, $crop_field) {
      // indicate if cropped area gets smaller than the specified minimal cropping
      var $jcrop_holder = $crop_field.siblings('.jcrop-holder');
      var min_width = $crop_field.data("min-width");
      var min_height = $crop_field.data("min-height");
      if ((sel.w < min_width) || (sel.h < min_height)) {
        $jcrop_holder.addClass('size-warning');
      } else {
        $jcrop_holder.removeClass('size-warning');
      }
    }

    return {
      init: init
    };

}(jQuery);

// init image cropping when DOM is ready
jQuery.noConflict(true)(function() {image_cropping.init();});
