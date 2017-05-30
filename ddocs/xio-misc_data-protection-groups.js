// view for xio misc docs
// returns data protection groups sub-jsons


function(doc) {

    var key ;


    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("xio_data-protection-groups_") != -1

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
        emit( key,  {"data-protection-groups":doc, "svt_action":"svt_multi"} );

    }
}