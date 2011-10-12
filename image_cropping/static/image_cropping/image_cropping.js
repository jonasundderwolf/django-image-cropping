$(function() {
  $('input.image-ratio').each(function() {
    var $this = $(this);
    // find the image field corresponding to this cropping value
    // by stripping the last part of our id and appending the image field name
    var field = $this.attr('name').replace($this.data('my-name'), $this.data('image-field'));

    // there should only be one file field we're referencing but in special cases
    // there can be several. Deal with it gracefully.
    var $image_input = $('input.crop-thumb[data-field-name=' + field + ']:visible:first');

    // skip this image if it's empty and hide the whole field
    if (!$image_input.length || $image_input.data('thumbnail-url') == undefined) {
      $this.parents('div.form-row:first').hide();
      return;
    }
    var image_id = $this.attr('id') + '-image';

    var org_width = $image_input.data('org-width')
    var org_height = $image_input.data('org-height')
    var min_width = $this.data('width');
    var min_height = $this.data('height');

    if ($this.data('adapt-rotation') == true) {
      if ($image.get(0).width < $image.get(0).height) {
        // cropping height/width need to be switched, picture is in portrait mode
        var x = min_width;
        min_width = min_height;
        min_height = x;
      }
    }
    var options = {
      parent: 'body',
      aspectRatio: min_width + ':' + min_height,
      minWidth: 5,
      minHeight: 5,
      imageWidth: org_width,
      imageHeight: org_height,
      handles: true,
      instance: true,
      onInit: update_selection($this),
      onSelectEnd: update_selection($this),
      cropping_allowed: (org_width > min_width) && (org_height > min_height)
    }

    // is the image bigger than the minimal cropping values?
    // otherwise lock cropping area on full image 
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

    // hide the input field, show image to crop instead
    $this.hide().after($('<img>', {
      'id': image_id,
      'src': $image_input.data('thumbnail-url'),
      'style': options.cropping_allowed ? '' : 'border:2px solid red'
    }));

    $this.data('imgareaselect', $('#' + image_id).imgAreaSelect(options));
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

  crop_indication(img, sel, $crop_field);
  $crop_field.val(new Array(
    sel.x1,
    sel.y1,
    sel.x2,
    sel.y2
  ).join(','));
}

function update_selection($crop_field) {
  return function(img, sel) { _update_selection(img, sel, $crop_field); };
}

function crop_indication(img, sel, $crop_field) {
  var min_width = $crop_field.data("width");
  var min_height = $crop_field.data("height");
  // indicate if cropped area gets smaller than the specified minimal cropping
  if ((sel.width < min_width) || (sel.height < min_height)) {
    $(img).css("border", "2px solid red");
  } 
}
