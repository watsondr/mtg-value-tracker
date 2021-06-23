$(document).ready(function(){
    $('[rel="popover"]').popover({
        html: true,
        placement : 'right',
        trigger : 'hover',
        content: function () {
        return '<img src="'+$(this).data('img') + '" />';
  }
    });
});