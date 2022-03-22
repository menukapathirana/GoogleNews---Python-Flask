var arr=[];
$('label.btn').on('click', function() {
    
    
            //Find the child check box.
            var $input = $(this).find('input');

            $(this).toggleClass('btn-danger btn-success');
            //Remove the attribute if the button is "disabled"
            if ($(this).hasClass('btn-danger')) {
               
                $input.attr('checked', '');
                arr.push($(this).text());
                
            } else {
               
                 $input.removeAttr('checked');
                arr.pop($(this).text());
            }
    

            return false; //Click event is triggered twice and this prevents re-toggling of classes
    
    
        });


/*

$(document).ready(function() {
    ("#mm").click(function(){
        alert(arr);

    });
});
*/





