// view for vcenter misc docs
// returns hosts sub-jsons



function(doc) {

    var key ;


    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vcenter_hosts.json") != -1
        
        ) {

        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single";


        // map all controllers
        key = [collect, client, source, id]  ;
        emit( key,  {"hosts":doc, "svt_action":"svt_single"} );

    }
}
