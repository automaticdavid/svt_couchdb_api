// view for rp4vm-system docs
// returns settings sub-jsons


function(doc) {

    var key ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("rp4vm_system-settings.json") != -1

        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single" ;

        // map all appliances
        key = [collect, client, source, id]  ;

        emit( key, {"settings":doc, 'svt_action':'svt_single'} );

    }
}