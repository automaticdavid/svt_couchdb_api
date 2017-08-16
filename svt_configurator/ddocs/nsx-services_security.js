// view for nsx-services docs
// returns security sub-jsons

function(doc) {

    var key ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("nsx_services-securitygroup-scope-globalroot-0.json") != -1
            && doc.svt_source_file.indexOf("nsx_services-securitytags-tag.json") == -1

        ) {

        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        file =  doc.svt_source_file ;
        filename = file.split("_")[2] ;
        id = filename.split(".")[0] ;

        key = [collect, client, source, id ]  ;
        emit( key, {"security" : doc, "svt_action":"svt_multi" } );


    }
}
