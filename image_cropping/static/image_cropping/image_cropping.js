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
    var width = $this.data('width');
    var height = $this.data('height');

    if ($this.data('adapt-rotation') == true) {
      if (image.width < image.height) {
        // cropping height/width need to be switched, picture is in portrait mode
        var x = width;
        width = height;
        height = x;
      }
    }
    var rx = 1000/image.width;
    var ry = 1000/image.height;
    var options = {
      parent: 'body',
      aspectRatio: width + ':' + height,
      minWidth: width / rx,
      minHeight: height / ry,
      handles: true,
      instance: true,
      onSelectEnd: update_selection($this)
    }
    var initial;
    if ($this.val()) {
      initial = initial_cropping($this.val(), rx, ry);
    } else {
      initial = max_cropping(width, height, image.width, image.height);
      // set cropfield to initial value
      $this.val(new Array(
        Math.round(initial.x1 * rx),
        Math.round(initial.y1 * ry),
        Math.round(initial.x2 * rx),
        Math.round(initial.y2 * ry)
      ).join(','));
    }
    $.extend(options, initial);
    $images.each(function() {
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

function initial_cropping(val, rx, ry) {
  if (val == '') { return; }
  var s = val.split(',');
  return {
    x1: Math.round(parseInt(s[0])/rx),
    y1: Math.round(parseInt(s[1])/ry),
    x2: Math.round(parseInt(s[2])/rx),
    y2: Math.round(parseInt(s[3])/ry)
  }
}

function _update_selection(img, sel, $crop_field) {
  var rx = 1000 / img.width;
  var ry = 1000 / img.height;
  $crop_field.val(new Array(
    Math.round(sel.x1 * rx),
    Math.round(sel.y1 * ry),
    Math.round(sel.x2 * rx),
    Math.round(sel.y2 * ry)
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
