// view for vra identity docs
// returns about sub-jsons



function(doc) {

    var key ;


    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vra_identity-about.json") != -1
        ) {

        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single";


        // map all controllers
        key = [collect, client, source, id]  ;
        emit( key,  {"about":doc, "svt_action":"svt_single"} );

    }
}
