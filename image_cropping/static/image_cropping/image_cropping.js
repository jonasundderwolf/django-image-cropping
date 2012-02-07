var image_cropping = {
  $: jQuery.noConflict(),
  init: function() {
    image_cropping.$('input.image-ratio').each(function() {
      var $this = image_cropping.$(this),
      // find the image field corresponding to this cropping value
      // by stripping the last part of our id and appending the image field name
          field = $this.attr('name').replace($this.data('my-name'), $this.data('image-field')),

      // there should only be one file field we're referencing but in special cases
      // there can be several. Deal with it gracefully.
          $image_input = image_cropping.$('input.crop-thumb[data-field-name=' + field + ']:first');

      // skip this image if it's empty and hide the whole field
      if (!$image_input.length || $image_input.data('thumbnail-url') == undefined) {
        $this.parents('div.form-row:first').hide();
        return;
      }
      var image_id = $this.attr('id') + '-image',
          org_width = $image_input.data('org-width'),
          org_height = $image_input.data('org-height'),
          min_width = $this.data('width'),
          min_height = $this.data('height');

      if ($this.data('adapt-rotation') == true) {
        if ($image.get(0).width < $image.get(0).height) {
          // cropping height/width need to be switched, picture is in portrait mode
          var x = min_width;
          min_width = min_height;
          min_height = x;
        }
      }
      var options = {
        aspectRatio: min_width/min_height,
        minSize: [5, 5],
        trueSize: [org_width, org_height],
        onSelect: image_cropping.update_selection($this)
      }
      // is the image bigger than the minimal cropping values?
      // otherwise lock cropping area on full image 
      var initial;
      if ($this.val()) {
        initial = image_cropping.initial_cropping($this.val());
      } else {

        initial = image_cropping.max_cropping(min_width, min_height, org_width, org_height);

          // set cropfield to initial value
        $this.val(initial.join(','));
      }

      image_cropping.$.extend(options, {setSelect: initial});

      // hide the input field, show image to crop instead
      $this.hide().after(image_cropping.$('<img>', {
        'id': image_id,
        'src': $image_input.data('thumbnail-url'),
        'style': ($this.data('size-warning') && ((org_width < min_width) || (org_height < min_height))) ? 'border:2px solid red': ''
      }));

      image_cropping.$('#' + image_id).Jcrop(options);
    });

    if (image_cropping.$('body').hasClass('change-form')) {
      // if we're in the Django admin, the holder needs to be floated
      // so it clears the label
      image_cropping.$("<style type='text/css'>div.jcrop-holder{float:left;}</style>").appendTo('head');
    }
  },
  max_cropping: function(width, height, image_width, image_height) {
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
  },
  initial_cropping: function(val) {
    if (val == '') { return; }
    var s = val.split(',');
    return [
      parseInt(s[0], 10),
      parseInt(s[1], 10),
      parseInt(s[2], 10),
      parseInt(s[3], 10)
    ];
  },
  _update_selection: function(sel, $crop_field) {
    if ($crop_field.data('size-warning')) {
      image_cropping.crop_indication(img, sel, $crop_field);
    }
    $crop_field.val(new Array(
      sel.x,
      sel.y,
      sel.x2,
      sel.y2
    ).join(','));
  },
  update_selection: function($crop_field) {
    return function(sel) { image_cropping._update_selection(sel, $crop_field); };
  },
  crop_indication: function(sel, $crop_field) {
    // indicate if cropped area gets smaller than the specified minimal cropping
    var min_width = $crop_field.data("width");
    var min_height = $crop_field.data("height");
    if ((sel.width < min_width) || (sel.height < min_height)) {
      image_cropping.$(img).css("border", "2px solid red");
    } else {
      image_cropping.$(img).css("border", "none");
    }
  }
};
image_cropping.$(function() {image_cropping.init();});
