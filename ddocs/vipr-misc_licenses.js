// view for vipr docs
// returns licenses sub-jsons


function(doc) {

    var key ;


    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vipr_license.json") != -1

        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single" ;


        // map all appliances
        key = [collect, client, source, id]  ;
        emit( key,  {"licenses":doc, "svt_action":"svt_single"} );

    }
}



