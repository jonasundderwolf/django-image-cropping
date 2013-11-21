var image_cropping = function ($) {

    function init() {
      // set styles for size-warning
      var style_img_warning = 'div.jcrop-image.size-warning .jcrop-vline{border:1px solid red; background: none;}' +
                              'div.jcrop-image.size-warning .jcrop-hline{border:1px solid red; background: none;}';
      $("<style type='text/css'>" + style_img_warning + "</style>").appendTo('head');

      $('input.image-ratio').each(function() {
        var $this = $(this),
        // find the image field corresponding to this cropping value
        // by stripping the last part of our id and appending the image field name
            field = $this.attr('name').replace($this.data('my-name'), $this.data('image-field')),

        // there should only be one file field we're referencing but in special cases
        // there can be several. Deal with it gracefully.
            $image_input = $('input.crop-thumb[data-field-name=' + field + ']:first');

        // skip this image if it's empty and hide the whole field, within admin and by itself
        if (!$image_input.length || $image_input.data('thumbnail-url') === undefined) {
          $this.hide().parents('div.form-row:first').hide();
          return;
        }
        // check if the image field should be hidden
        if ($image_input.data('hide-field')) {
          $image_input.hide().parents('div.form-row:first').hide();
        }

        var image_id = $this.attr('id') + '-image',
            org_width = $image_input.data('org-width'),
            org_height = $image_input.data('org-height'),
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
          'src': $image_input.data('thumbnail-url')
        });

        var options = {
          minSize: [5, 5],
          keySupport: false,
          trueSize: [org_width, org_height],
          onSelect: update_selection($this),
          addClass: ($this.data('size-warning') && ((org_width < min_width) || (org_height < min_height))) ? 'size-warning jcrop-image': 'jcrop-image'
        };
        if ($this.data('ratio')) {
          options['aspectRatio'] = $this.data('ratio');
        }

        var cropping_disabled = false;
        if($this.val()[0] == "-"){
          cropping_disabled = true;
          $this.val($this.val().substr(1));
        }

        // is the image bigger than the minimal cropping values?
        // otherwise lock cropping area on full image
        var initial;
        if ($this.val()) {
          initial = initial_cropping($this.val());
        } else {

          initial = max_cropping(min_width, min_height, org_width, org_height);

            // set cropfield to initial value
          $this.val(initial.join(','));
        }

        $.extend(options, {setSelect: initial});

        // hide the input field, show image to crop instead
        $this.hide().after($image);

        var jcrop = {};

        $('#' + image_id).Jcrop(options, function(){jcrop[image_id]=this;});

        if ($this.data('allow-fullsize') === true) {
          if(cropping_disabled){
            jcrop[image_id].release();
            $this.val('-'+$this.val());
          }
          var label = 'allow-fullsize-'+image_id;
          var checked = cropping_disabled ? '' : ' checked="checked"';
          $('<div class="field-box allow-fullsize">' +
                           '<input type="checkbox" id="'+label+'" name="'+label+'"'+checked+'></div>').appendTo($this.parent());
          $('<style type="text/css">div.allow-fullsize{padding: 5px 0 0 10px;}</style>').appendTo('head');
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

      if ($('body').hasClass('change-form')) {
        // if we're in the Django admin, the holder needs to be floated
        // so it clears the label
        $("<style type='text/css'>div.jcrop-holder{float:left;}</style>").appendTo('head');
      }
    }

    function max_cropping (width, height, image_width, image_height) {
      var ratio = width/height;
      var offset;

      if (image_width < image_height * ratio) {
        // width fits fully, height needs to be cropped
        offset = Math.round((image_height-(image_width/ratio))/2);
        return [0, offset, image_width, image_height - offset];
      }
      // height fits fully, width needs to be cropped
      offset = Math.round((image_width-(image_height * ratio))/2);
      return [offset, 0, image_width - offset, image_height];
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
