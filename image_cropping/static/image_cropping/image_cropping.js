$(window).load(function() {
  $('input.image-ratio').each(function() {
    // find the image field corresponding to this cropping value
    // by stripping the last part of our id and appending the image field name
    var $this = $(this);
    $this.parents('div.form-row:first').hide();
    var field = $this.attr('name').replace($this.data('my-name'), $this.data('image-field'));
    var $images = $('img.admin-thumb[data-field-name=' + field + ']:visible');
    if (!$images.length) {return;}
    var image = $images.get(0);
    var org_width = $(image).data('org-width')
    var org_height = $(image).data('org-height')
    var min_width = $this.data('width');
    var min_height = $this.data('height');

    if ($this.data('adapt-rotation') == true) {
      if (image.width < image.height) {
        // cropping height/width need to be switched, picture is in portrait mode
        var x = min_width;
        min_width = min_height;
        min_height = x;
      }
    }
    var options = {
      parent: 'body',
      aspectRatio: min_width + ':' + min_height,
      minWidth: min_width,
      minHeight: min_height,
      imageWidth: org_width,
      imageHeight: org_height,
      handles: true,
      instance: true,
      onSelectEnd: update_selection($this)
    }

    var cropping_allowed = ((org_width > min_width) && (org_height > min_height)) 
    options.cropping_allowed = cropping_allowed;

    // if the image is smaller than the minimal cropping warn the user
    // but allow a smaller cropping. we use a fixed minimal size to prevent
    // negative values (that result in a crazy selection behaviour).

    if (!cropping_allowed) {
      options.minWidth = 30;
      options.minHeight = 30;
    };
   
    // is the image bigger than the minimal cropping values?
    // other lock cropping area on full image 
    var initial;
    if ($this.val()) {
      initial = initial_cropping($this.val());
    } else {

      initial = max_cropping(min_width, min_height, org_width, org_height);

        // set cropfield to initial value
      $this.val(new Array(
        initial.x1,
        initial.y1,
        initial.x2,
        initial.y2
      ).join(','));
    }

    $.extend(options, initial);

    $images.each(function() {
      if (!options.cropping_allowed) {
        $(this).css("border", "solid 2px red");
      }
      $(this).data('imgareaselect', $(this).imgAreaSelect(options));
    });
  });
});

function max_cropping(width, height, image_width, image_height) {
  var ratio = width/height;
  var offset;

  if (image_width < image_height * ratio) {
    // width fits fully, height needs to be cropped
    offset = Math.round((image_height-(image_width/ratio))/2);
    return {
      x1: 0,
      y1: offset,
      x2: image_width,
      y2: image_height - offset
    }
  }
  // height fits fully, width needs to be cropped
  offset = Math.round((image_width-(image_height * ratio))/2);
  return {
    x1: offset,
    y1: 0,
    x2: image_width - offset,
    y2: image_height
  }
}

function initial_cropping(val) {
  if (val == '') { return; }
  var s = val.split(',');
  return {
    x1: parseInt(s[0]),
    y1: parseInt(s[1]),
    x2: parseInt(s[2]),
    y2: parseInt(s[3])
  }
}

function _update_selection(img, sel, $crop_field) {

  $crop_field.val(new Array(
    sel.x1,
    sel.y1,
    sel.x2,
    sel.y2
  ).join(','));

  $('img.admin-thumb[data-field-name=' + $(img).data('field-name')+ ']:visible').each(function() {
    var ias = $(this).data('imgareaselect');
    if (ias !== undefined) {
      ias.setSelection(sel.x1, sel.y1, sel.x2, sel.y2, true);
      ias.update();
    }
  });
}

function update_selection($crop_field) {
  return function(img, sel) { _update_selection(img, sel, $crop_field); };
}
