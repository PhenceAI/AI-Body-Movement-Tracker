$(".s_btn").click(function(){

    btn_text = $(".s_btn").text()
    if (btn_text == "Start"){
        $fname = $(".filename_inp").val()
        if ($fname==""){
            alert("Please enter a filename first!")
        }else{
            change_filename_and_start_cam($fname)
        }
        
    }else if (btn_text == "Stop"){
        $(".box").empty();
        $(".box").css("opacity", 0.4)
        $(".s_btn").text("Start");
        $(".filename_inp").val("")
    }

    
});

function change_filename_and_start_cam(filename){
    // sending an ajax request to change filename
    loc = window.location.href + "change_filename";
    $.ajax({ 
        url: loc ,
        type: 'POST', 
        data: filename + ".csv",
        success: function(response){ 
            $(".box").append('<img src="/video_feed" width="100%">');
            $(".box").css("opacity", 1)
            $(".s_btn").text("Stop");
        } 
    })

}