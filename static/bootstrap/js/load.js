        $(document).ready(function(){
            $("#quarter_dropdown").change(function(){
                $(this).find("option:selected").each(function(){
                    var optionValue = $(this).attr("value");
                    if(optionValue == "4"){
                        $("#clutch_time").show();
                    }

                    else{
                        $("#clutch_time").hide();
                    }
                });
            }).change();
        });