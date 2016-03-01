/**
 * Created by david on 05/01/16.
 */
$(document).ready(function() {
    $('#play').on('click',function(){
        var i= 30, min = 0, delay = 2500, run;
        run= function(){
            document.getElementById("time_filter").value = "" + i;
            updateSlider();
            if(i-- > min){
                setTimeout(run, delay);
            }
        }
        run();
        return false;
    });
});

