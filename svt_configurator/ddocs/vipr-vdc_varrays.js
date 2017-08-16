// view for vipr vdc docs
// returns varrays sub-jsons


function(doc) {

    var key ;


    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vipr_vdc-varrays_") != -1

        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        file =  doc.svt_source_file ;
        filename = file.split("_")[2] ;
        id = filename.split(".")[0] ;


        // map all appliances
        key = [collect, client, source, id]  ;
        emit( key,  {"varrays":doc, "svt_action":"svt_multi"} );

    }
}
