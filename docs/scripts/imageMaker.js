

function fancyMenuHover(evt){
    alert(evt)
    $("#agriculture_table img").each(function (){
        sourceFile = $(this).attr("src")
        if (sourceFile.includes("/"+ evt + "/")){
            $(this).parent().removeClass('agri_unselected')
            $(this).parent().addClass('agri_selected')
        }else{
            $(this).parent().removeClass('agri_selected')
            $(this).parent().addClass('agri_unselected')

        }

    });


}