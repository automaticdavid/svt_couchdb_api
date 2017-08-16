// view for vrops suite docs
// returns api versions sub-jsons



function(doc) {

    var key ;


    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vrops_suite-api-api-versions-current.json") != -1
        ) {

        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single";


        // map all controllers
        key = [collect, client, source, id]  ;
        emit( key,  {"api-versions":doc, "svt_action":"svt_single"} );

    }
}
