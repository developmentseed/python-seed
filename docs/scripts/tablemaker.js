function transpose(a) {
    return Object.keys(a[0]).map(function(c) {
        return a.map(function(r) { return r[c]; });
    });
}

var tableContent = transpose([

    [   "plant/plough.gif"
        ,"plant/seed_and_sprout.gif"
        ,"plant/seed_sprouting.gif"
        ,"plant/sunny_sprout.gif"
        ,"plant/seeding_trailer.gif"
        ,"plant/wheat_seedling.gif"
    ]

    ,[  "feed/raindrops.gif"
        ,"feed/irrigation_pipe.gif"
        ,"feed/airplane_irrigation.gif"
        ,"feed/raindrop_with_cog.gif"
        ,"feed/feed_spreader.gif"
        ,"feed/raindrops.gif"


    ]

    ,["develop/measure_height.gif"
        ,"develop/seed_lab.gif"
        ,"develop/seed_time.gif"
        ,"develop/chemicals.gif"
        ,"develop/measure_height.gif"
        ,"develop/hay_bail.gif"

    ]


    ,["harvest/combine_harvester.gif"
        ,"harvest/bailing_tractor.gif"
        ,"harvest/grain_silo.gif"
        ,"harvest/thresher_trailer.gif"
        ,"harvest/mini_harvester.gif"
        ,"harvest/distillery.gif"

    ]


]);

$(document).ready(function(){
    createTable()
});



function createTable(){

    tableElement = document.createElement("table");
    tableContent.forEach(function(thisrow){
        rowElement = document.createElement("tr");
         tableElement.append(rowElement);
        thisrow.forEach(function(thisCol){
            colElement =  document.createElement("td")
            colElement.classList.add('agri_unselected')
            rowElement.append(colElement);
            imgElement = document.createElement("img");
            imgElement.setAttribute("src", "webimg/tiles/named/" + thisCol)
            colElement.append(imgElement)
        })
    })

    $("#agriculture_table").append(tableElement)


}


function fancyMenuHover(evt){
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